# 📄 PubMed Fetcher

A Python command-line tool to fetch research papers from PubMed, filter out those with non-academic authors, and save results as a CSV file.

## 📌 Features
✅ Fetches research papers from PubMed using a query.  
✅ Filters papers with at least one non-academic author (e.g., biotech/pharma companies).  
✅ Saves results as a CSV file with key paper details.  
✅ Provides a command-line interface with flexible options.  
✅ Uses Poetry for dependency management.  

## 🛠 Prerequisites
Ensure you have the following installed:

1️⃣ Python 3.8+ (Recommended: Latest stable version)  
2️⃣ Poetry (For dependency management)  
3️⃣ Git (To clone the repository)  

## 📥 Installation & Setup

### 1️⃣ Clone the Repository
Open your terminal (or PowerShell) and run:

```sh
git clone https://github.com/your-username/pubmed-fetcher.git
cd pubmed-fetcher
```

### 2️⃣ Install Poetry
If you don’t have Poetry installed, run:

```sh
pip install poetry
```

After installation, check if Poetry is working:

```sh
poetry --version
```

### 3️⃣ Install Dependencies
Run the following command inside the project directory:

```sh
poetry install
```

This will create a virtual environment and install all required dependencies.

### 4️⃣ Activate Virtual Environment
Run this command:

```sh
poetry shell
```

This ensures you're running the project inside the correct environment.

## 🚀 Usage

### 1️⃣ Run the CLI Command
The tool provides a CLI interface to fetch PubMed papers. Use the following syntax:

```sh
poetry run get-papers-list "your_query_here" -f output.csv
```

### 📌 Example
To fetch papers related to "cancer treatment" and save results to `results.csv`:

```sh
poetry run get-papers-list "cancer treatment" -f results.csv
```

### 🔧 CLI Options

| Option  | Description  |
|---------|-------------|
| `-h, --help` | Show help message and usage details |
| `-d, --debug` | Enable debug mode for detailed logs |
| `-f, --file` | Specify the output CSV file name |

## 📂 Project Structure

```bash
pubmed-fetcher/
│── src/
│   ├── pubmed_fetcher/
│   │   ├── fetcher.py  # Core logic to fetch papers
│   │   ├── cli.py      # Command-line interface script
│   │   ├── utils.py    # Helper functions
│   ├── tests/          # Unit tests
│── pyproject.toml      # Poetry config file
│── README.md           # Project documentation
│── .gitignore          # Ignore unnecessary files
```

