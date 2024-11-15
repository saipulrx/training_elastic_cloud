# Snippet for Day 2 Module 4 Searching in Elastic Search(DSL)

## <em>Quick links to the recipes</em>
* [Searching with the Query DSL ](#searching-with-the-query-dsl)
* [Building advanced search query with Query DSL](#building-advanced-search-query-with-query-dsl)
* [Nested Query](#nested-query)
* [Relevance Score](#relevance-score)

## Ingest data to Elastic Search
Run python code upload_csv.py in python_client folder before search with query DSL. Adjust with your, elastic cloud environment and dataset

## Searching with the Query DSL
This Query use dataset superstore.csv
### Sample Query DSL with Match All
```
GET /superstore/_search
{
  "query": {
    "match_all": {}
  }
}
```
### Sample Query DSL with Match
```
GET /superstore/_search
{
  "query": {
    "match": {
      "Category":"furniture"
    }
  }
}
```
### Sample Query DSL with Match & AND operator
```
GET /superstore/_search
{
  "query": {
    "match": {
      "Category":{
        "query": "supplies",
        "operator": "and"
      }
    }
  }
}
```

### Sample Query DSL with Multi Match
```
GET /superstore/_search
{
  "query": {
    "multi_match": {
      "query":"united",
      "fields": ["Country","City"]
    }
  }
}
```

### Sample Query DSL with Query String
```
GET /superstore/_search
{
  "query": {
    "query_string": {
      "query":"west"
    }
  }
}
```

### Sample Query DSL with Term
```
GET /superstore/_search
{
  "query": {
    "term": {
      "Quantity":14
    }
  }
}
```

### Sample Query DSL Range Query - Greater than equal(gte)
```
GET /superstore/_search
{
  "query": {
    "range": {
      "Quantity": {
        "gte": 10
      }
    }
  }
}
```

## Building advanced search query with Query DSL

### Range Query
```
GET /superstore/_search
{
  "query": {
    "range": {
      "Quantity": {
        "gte": 10,
        "lte": 11
      }
    }
  }
}
```

### Boolean Query
```
GET /superstore/_search
{
  "query": 
  {
    "bool": 
    {
      "must": 
      [
        {"match": {
          "Sub-Category": "appliances"
        }},
        {
          "match": {
            "Region": "west"
          }
        }
      ]
    }
  }
}
```

### Boolean Query with Filter
```
GET /superstore/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {
          "Sub-Category": "appliances"
        }}
      ],
      "filter": [
        {"match":{
          "Segment":"consumer"
        }}
      ]
    }
  }
}
```

### Fuzzy Search
```
GET /superstore/_search
{
  "query": {
    "fuzzy": {
      "Segment": {
        "value": "cansamer",
        "fuzziness": 2
      }
    }
  }
}
```

### Proximity Search
```
GET /superstore/_search
{
  "query": {
    "match_phrase": {
      "Product Name": {
        "query":"wood plastic",
        "slop": 2
      }
    }
  }
}
```

## Nested Query
For demo nested query, please click [this](https://github.com/saipulrx/training_elastic_cloud/tree/main/Day2_Module4/nested_query.md)
## Relevance Score
### Using the explain Parameter for Score Explanation
```
GET /superstore/_search
{
  "explain": true,
  "query": {
    "match": {
      "Category": "supplies"
      }
    }
  }
```

### multi_match Query with Field Boosting
```
GET /superstore/_search  
{
  "query": {
    "multi_match": {
      "query": "corporate",
      "fields": ["Segment^3", "Category"]
    }
  }
}
```

### Bool query with boosting
```
GET /superstore/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "Segment": "corporate" } }
      ],
      "should": [
        { "match": { "Region": "west" } }
      ],
      "boost": 2.0
    }
  }
}
```
### function_score Query for Custom Scoring
```
GET /superstore/_search
{
  "query": {
    "function_score": {
      "query": {
        "match": {
          "Segment": "corporate"
        }
      },
      "boost_mode": "multiply",
      "functions": [
        {
          "field_value_factor": {
            "field": "Sales",
            "factor": 1.2,
            "modifier": "log1p"
          }
        }
      ]
    }
  }
}
```

### script_score Query for Custom Scripting
```
GET /superstore/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
          "Segment": "corporate"
        }
      },
      "script": {
        "source": "_score + doc['Sales'].value * 0.1"
      }
    }
  }
}
```