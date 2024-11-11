## Nested Query
### Example Scenario
Let's say you have an index of e-commerce products, and each product has multiple reviews. Each review has attributes like username, rating, and comment. You want to search for products based on specific attributes of reviews, such as finding products where a specific user gave a certain rating.

#### Step 1 : Create an Index with a Nested Field
Let's create an index named products with a nested field for reviews:
```
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "category": {
        "type": "keyword"
      },
      "reviews": {
        "type": "nested",
        "properties": {
          "username": {
            "type": "keyword"
          },
          "rating": {
            "type": "integer"
          },
          "comment": {
            "type": "text"
          }
        }
      }
    }
  }
}
```
In the above mapping:
The reviews field is defined as nested, meaning each review object is treated separately.

#### Step 2 : Insert Sample Documents
Now, let's insert some sample products with reviews:
```
POST /products/_bulk
{"index": {"_id": 1}}
{"name": "Smartphone A", "category": "Electronics", "reviews": [{"username": "user1", "rating": 5, "comment": "Excellent phone!"}, {"username": "user2", "rating": 4, "comment": "Good value for money."}]}
{"index": {"_id": 2}}
{"name": "Laptop B", "category": "Electronics", "reviews": [{"username": "user3", "rating": 4, "comment": "Great performance."}, {"username": "user1", "rating": 3, "comment": "Average battery life."}]}
{"index": {"_id": 3}}
{"name": "Headphones C", "category": "Accessories", "reviews": [{"username": "user2", "rating": 2, "comment": "Poor sound quality."}, {"username": "user4", "rating": 5, "comment": "Amazing sound!"}]}
```

#### Step 3 : Running a Nested Query
Suppose you want to find products where user1 gave a rating of 3. This requires a nested query since we need to match these conditions within the same review object.
```
GET /products/_search
{
  "query": {
    "nested": {
      "path": "reviews",
      "query": {
        "bool": {
          "must": [
            { "match": { "reviews.username": "user1" }},
            { "match": { "reviews.rating": 3 }}
          ]
        }
      },
      "inner_hits": {}
    }
  }
}
```
Explanation:

* nested: Specifies that we're querying the reviews field, which is nested.
* path: Indicates the path to the nested field (reviews).
* bool query: Ensures that both conditions (username is user1 and rating is 3) match within the same nested review object.
* inner_hits: Returns the specific matching nested objects within the parent document.

Expected Output
```
{
  "hits": {
    "hits": [
      {
        "_id": "2",
        "_source": {
          "name": "Laptop B",
          "category": "Electronics",
          "reviews": [
            {"username": "user3", "rating": 4, "comment": "Great performance."},
            {"username": "user1", "rating": 3, "comment": "Average battery life."}
          ]
        },
        "inner_hits": {
          "reviews": {
            "hits": {
              "hits": [
                {
                  "_source": {
                    "username": "user1",
                    "rating": 3,
                    "comment": "Average battery life."
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```
Explanation of the Results:

* The query returns only one product (Laptop B) because that's where user1 gave a rating of 3.
* The inner_hits section shows the exact review that matched the query conditions.