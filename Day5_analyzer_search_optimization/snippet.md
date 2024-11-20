# Snippet for Day 5 Module Analyzer and Search Optimization

## <em>Quick links to the recipes</em>
* [Example Tokenization and Normalization](#example-tokenization-and-normalization)
* [Example Standar Tokenizer](#example-standar-tokenizer)
* [Example Ngram Tokenizer](#example-ngram-tokenizer)
* [Example Edge Ngram Tokenizer](#example-edge-ngram-tokenizer)
* [Built in Analyzer](#built-in-analyzer)
* [Custom Analyzer and Compare with default Analyzer](#custom-analyzer-and-compare-with-default-analyzer)


## Example Tokenization and Normalization
This example for process english text

Step 1 : Create index and define analyzer
```
PUT test_english_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_english_analyzer": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "stop"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "analyzer": "my_english_analyzer"
      }
    }
  }
}
```
Explanation:

1. Index Creation: We create an index named my_index.
2. Analyzer Definition:
    - my_english_analyzer:
        - tokenizer: standard - Breaks text into words based on word boundaries.
        - filter:
lowercase: Converts all tokens to lowercase.
        - stop: Removes common words (stop words) that don't add significant meaning to the search.

Step 2 : Indexing a document
```
POST my_index/_doc
{
  "text": "This is a sample text for testing Elasticsearch."
}
```

Step 3 : Searching the index
```
GET my_index/_search
{
  "query": {
    "match": {
      "text": "sample text"
    }
  }
}
```

## Example Standar Tokenizer
```
POST /_analyze
{
  "tokenizer": "standard",
  "text": "The quick-brown fox jumps over lazy dogs. Email: example@test.com"
}
```

## Example of Ngram Tokenizer
Use Case:
Useful for fuzzy matching or substring search.
- Create an Index with N-gram Tokenizer:
```
PUT /ngram_example
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "ngram_tokenizer": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      },
      "analyzer": {
        "ngram_analyzer": {
          "type": "custom",
          "tokenizer": "ngram_tokenizer",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "ngram_analyzer"
      }
    }
  }
}
```
- Test the N-gram Tokenizer:
```
POST /ngram_example/_analyze
{
  "analyzer": "ngram_analyzer",
  "text": "hello"
}
```

## Example Edge Ngram Tokenizer
Use Case:
Useful for autocomplete or search-as-you-type.
- Create an Index with Edge N-gram Tokenizer:
```
PUT /edge_ngram_example
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "edge_ngram_tokenizer": {
          "type": "edge_ngram",
          "min_gram": 2,
          "max_gram": 3
        }
      },
      "analyzer": {
        "edge_ngram_analyzer": {
          "type": "custom",
          "tokenizer": "edge_ngram_tokenizer",
          "filter": ["lowercase"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "edge_ngram_analyzer"
      }
    }
  }
}
```

- Test the Edge N-gram Tokenizer:
```
POST /edge_ngram_example/_analyze
{
  "analyzer": "edge_ngram_analyzer",
  "text": "hello"
}
```

## Built in Analyzer
### Standar Analyzer(default)
```
POST /_analyze
{
  "analyzer": "standar",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```
### Simple Analyzer
```
POST /_analyze
{
  "analyzer": "simple",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```
### Whitespace Analyzer
```
POST /_analyze
{
  "analyzer": "whitespace",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```
### Keyword Analyzer
```
POST /_analyze
{
  "analyzer": "keyword",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```
### Stop Analyzer
```
POST /_analyze
{
  "analyzer": "stop",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```
### Language Analyzer (English)
```
POST /_analyze
{
  "analyzer": "english",
  "text": "The Quick Brown Fox jumps-over 123 times!"
}
```

## Custom Analyzer and Compare with default Analyzer
Step 1 : Create an index with a custom analyzer PUT
```
PUT /text_analysis_demo
{
  "settings": {
    "analysis": {
      "analyzer": {
        "demo_analyzer": {
          "type": "custom",
          "char_filter": ["html_strip"],
          "tokenizer": "standard",
          "filter": ["lowercase", "stop"]
        }
      }
    }
  }
}
```

Step 2 : Analyze some sample text
```
POST /text_analysis_demo/_analyze
{
  "analyzer": "demo_analyzer",
  "text": "<p>The Quick Brown Fox Jumps Over the Lazy Dog</p>"
}
```

Step 3 : Analyze text with the default analyzer for comparison
```
POST /_analyze
{
  "analyzer": "standard",
  "text": "The Quick Brown Fox Jumps Over the Lazy Dog"
}
```

<b>Explanation</b>

Step 1 : Create an Index:

The custom analyzer, demo_analyzer, includes:
- html_strip character filter: Strips HTML tags.
- standard tokenizer: Splits text into tokens based on language rules.
- lowercase filter: Converts all tokens to lowercase.
- stop filter: Removes common stop words (like "the", "over").

Step 2 : Analyze Text with Custom Analyzer:

The _analyze API applies the demo_analyzer to the input text: <p>The Quick Brown Fox Jumps Over the Lazy Dog</p>

Step 3 : Analyze Text with Default Analyzer:

For comparison, the _analyze API uses the default standard analyzer to process the same text.