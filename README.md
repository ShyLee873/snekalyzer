# 🐍 Snekalyzer  
*A tool for analyzing Rails logs.*

Snekalyzer crawls through your `development.log` or `test.log` and reports:

- Slowest endpoints  
- Average request time  
- Average DB time  
- Request counts  
- Status codes  

For the Rails dev who wants quick performance insights without spinning up heavy tools.

---

## Installation

1. Clone this folder or copy it into your project.
2. Run with Python 3.9+.

No external packages required!

---

## Usage

### Analyze a Rails log

```bash
python analyze_logs.py /path/to/rails-app/log/development.log
```

### Show more or fewer results
```bash
python analyze_logs.py /path/to/log --top 20
```

## How It Works
- Parses "Started..." lines to grab the URL.
- Matches "Completed...in XYZms" lines to capture timing.
- Aggregates stats and prints the slowest endpoints.

## 🐍 Why “Snekalyzer”?
2 reasons:
- Because snakes analyze logs.
- Because I like snakes. 

Happy slithering!!