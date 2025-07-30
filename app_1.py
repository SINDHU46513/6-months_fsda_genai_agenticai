import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ollama
import os # Used for creating directories and managing plot files

# Function to Perform EDA and Generate Visualizations
def eda_analysis(file_path):
    """
    Performs Exploratory Data Analysis (EDA) on an uploaded CSV file,
    including data summary, missing value handling, AI-powered insights,
    and data visualizations.

    Args:
        file_path (str): The temporary path to the uploaded CSV file.

    Returns:
        tuple: A tuple containing:
            - str: The EDA report text.
            - list: A list of paths to the generated plot images.
    """
    # 1. Handle case where no file is uploaded
    if file_path is None:
        return "Please upload a CSV file to begin the analysis.", []

    df = None
    # 2. Robust CSV Reading: Try different encodings to handle common issues
    # This loop attempts to read the CSV with various common encodings.
    # If one succeeds, it breaks the loop. If all fail, df remains None.
    encodings_to_try = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1']
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read CSV with encoding: {encoding}")
            break # Exit loop if reading is successful
        except (UnicodeDecodeError, pd.errors.ParserError) as e:
            print(f"Failed to read with encoding {encoding}: {e}")
            continue # Try the next encoding
        except Exception as e:
            # Catch any other unexpected errors during file reading
            print(f"An unexpected error occurred while reading with encoding {encoding}: {e}")
            continue
    
    # If df is still None after trying all encodings, return an error message
    if df is None:
        return (
            "Error: Could not read the CSV file. "
            "Please ensure it's a valid CSV file and check its formatting (e.g., delimiter, special characters). "
            "You might need to save the CSV with UTF-8 encoding or a compatible format."
        ), []

    # 3. Handle Missing Values: Fill with median for numeric, mode for categorical
    # Addressing FutureWarning by reassigning the column instead of using inplace=True
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())
    
    for col in df.select_dtypes(include=['object']).columns:
        # .mode()[0] handles cases where mode might return multiple values
        df[col] = df[col].fillna(df[col].mode()[0])
    
    # Generate Data Summary
    summary = df.describe(include='all').to_string()
    
    # Generate Missing Values Report
    missing_values = df.isnull().sum().to_string()

    # Generate AI Insights using Ollama
    insights = generate_ai_insights(summary)
    
    # Generate Data Visualizations
    plot_paths = generate_visualizations(df)
    
    # Construct the final EDA report
    report = (
        f"Data Loaded Successfully!\n\n"
        f"--- Data Summary ---\n{summary}\n\n"
        f"--- Missing Values Handled ---\n{missing_values}\n\n"
        f"--- AI Insights ---\n{insights}"
    )
    
    return report, plot_paths

# AI-Powered Insights using Mistral (Ollama)
def generate_ai_insights(df_summary):
    """
    Generates AI-powered insights from a DataFrame summary using Ollama.

    Args:
        df_summary (str): The string representation of the DataFrame's summary statistics.

    Returns:
        str: The AI-generated insights or an error message if Ollama fails.
    """
    prompt = f"Analyze the following dataset summary and provide concise, actionable insights, highlighting key observations, potential anomalies, or interesting distributions. Focus on the meaning of the statistics:\n\n{df_summary}"
    try:
        # 4. Ollama Memory Error Handling: Catch specific Ollama errors
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except ollama.ResponseError as e:
        # Check for the specific memory error message
        if "requires more system memory" in str(e):
            return (
                f"AI Insight Generation Failed: The 'mistral' model requires more system memory "
                f"than is available on your system. Please consider using a smaller Ollama model "
                f"(e.g., 'tinyllama', 'phi', 'gemma:2b') or running Ollama on a machine with more RAM. "
                f"Error details: {e}"
            )
        else:
            # Handle other types of Ollama API errors
            return f"AI Insight Generation Failed: An Ollama API error occurred. Please check your Ollama server status and model availability. Error details: {e}"
    except Exception as e:
        # Catch any other unexpected errors during AI insight generation
        return f"AI Insight Generation Failed: An unexpected error occurred during AI processing: {e}"

# Function to Generate Data Visualizations
def generate_visualizations(df):
    """
    Generates common data visualizations (histograms, correlation heatmap)
    and saves them as PNG files.

    Args:
        df (pd.DataFrame): The DataFrame to visualize.

    Returns:
        list: A list of file paths to the generated plot images.
    """
    plot_paths = []
    
    # Create a directory to store the plots to keep the working directory clean
    plots_dir = "eda_plots"
    os.makedirs(plots_dir, exist_ok=True) # Creates the directory if it doesn't exist

    # Histograms for Numeric Columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        plt.figure(figsize=(8, 5)) # Set a good figure size
        sns.histplot(df[col], bins=30, kde=True, color="skyblue") # Use a pleasant color
        plt.title(f"Distribution of {col}", fontsize=14)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a grid for readability
        path = os.path.join(plots_dir, f"{col}_distribution.png")
        plt.savefig(path, bbox_inches='tight') # bbox_inches='tight' prevents labels/titles from being cut off
        plt.close() # Close the plot to free up memory
        plot_paths.append(path)
    
    # Correlation Heatmap (only for numeric columns, if there are at least two)
    if not numeric_cols.empty and len(numeric_cols) > 1:
        plt.figure(figsize=(10, 8)) # Larger figure for better readability of heatmap
        sns.heatmap(
            df[numeric_cols].corr(), # Calculate correlation only for numeric columns
            annot=True,              # Show correlation values on the heatmap
            cmap='viridis',          # Choose a color map
            fmt=".2f",               # Format annotations to two decimal places
            linewidths=0.5,          # Add lines between cells
            linecolor='black'        # Color of the lines
        )
        plt.title("Correlation Heatmap", fontsize=16)
        path = os.path.join(plots_dir, "correlation_heatmap.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        plot_paths.append(path)
    elif len(numeric_cols) <= 1:
        print("Skipping correlation heatmap: Not enough numeric columns (need at least 2).")

    return plot_paths

# Gradio Interface Definition
demo = gr.Interface(
    fn=eda_analysis,
    inputs=gr.File(type="filepath", label="Upload CSV File"), # Added a clear label for the input
    outputs=[gr.Textbox(label="EDA Report"), gr.Gallery(label="Data Visualizations")],
    title="📊 LLM-Powered Exploratory Data Analysis (EDA)",
    description=(
        "Upload any dataset CSV file and get automated EDA insights with AI-powered analysis and visualizations. "
        "**Important:** Ensure your Ollama server is running and the 'mistral' model is downloaded (`ollama pull mistral`). "
        "If you encounter memory errors with 'mistral', consider using a smaller model like 'tinyllama', 'phi', or 'gemma:2b'."
    )
)

# Launch the Gradio App
demo.launch(share=True)