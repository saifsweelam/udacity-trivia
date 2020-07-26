# API Documentations

## Getting Started

* This API service is hosted locally to the domain `http://localhost:5000` and it should be used in all of the API Endpoints.
* This app doesn't require any Authentication and doesn't require an API key.
* This app uses `CORS` Policy to allow cross-domain requests.
****

## Error Handling

_This app returns the following errors when needed:_
* `400` : Bad Request _(When the arguments or data you send to the server are invalid)_
* `404` : Resource Not Found _(When you try to access a resource which can't be found)_
* `405` : Method Not Allowed _(When you try to send a request whose method isn't handled)_
* `422` : Unprocessable _(When you send data that makes returning a valid response impossible)_
* `500` : Internal Server Error _(When there's a problem resolving your request by the server)_

### Error Sample Response

```json
{
  "message": "Resource Not Found", 
  "status_code": 404, 
  "success": false
}
```
****

## Endpoints


### GET `/categories`
* Gets a list of all categories.
* **TAKES NO PARAMETERS**

#### Sample Request
```shell
$ curl 'http://localhost:5000/categories'
```

#### Sample Response
```json
{
  "success": true,
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ]
}
```


### GET `/questions`
* Gets a list of 10 questions per page.
* **URL PARAMETERS:**

|Paremeter|description              |default|
|---------|-------------------------|-------|
|page     |specifies the page number|1      |

#### Sample Request
```shell
$ curl 'http://localhost:5000/questions?page=2'
```

#### Sample Response
```json
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "current_category": "ALL", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```


### DELETE `/questions/<int:question_id>`
* Deletes a question from the database. If the question wasn't found, it returns a `404` error.
* **TAKES NO PARAMETERS**

#### Sample Request
```shell
$ curl -X DELETE 'http://localhost:5000/questions/12'
```

#### Sample Response
```json
{
  "success": true,
  "question_id": 12
}
```


### POST `/questions`
* If a search term is provided, it searches for this term in the questions.
* If a question details are provided, it adds a new question to the database.
* If any of the data is missing, it sends a `400` error.
* **BODY DETAILS:**

_For Searching_
|key       |description                                               |required|
|----------|----------------------------------------------------------|--------|
|searchTerm|the term that will be matched to questions in the database|true    |

_For Adding_
|key       |description                   |required|
|----------|------------------------------|--------|
|question  |title of the question         |true    |
|answer    |answer of the question        |true    |
|difficulty|difficulty of the question    |true    |
|category  |id of category of the question|true    |

#### Sample Request
```shell
$ curl -H 'Content-Type: application/json' \
       -X POST \
       -d '{"searchTerm": "movie"}' \
       'http://localhost:5000/questions'

$ curl -H 'Content-Type: application/json' \
       -X POST \
       -d '{"question": "How are you?", "answer": "I am fine", "difficulty": 3, "category": 2}' \
       'http://localhost:5000/questions'
```

#### Sample Response
_For Searching_
```json
{
  "current_category": "Search", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```
_For Adding_
```json
{
  "success": true,
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }
}
```


### GET `/categories/<int:category_id>/questions`
* Gets questions of a specific category.
* If category doesn't exist, it returns `404` error.
* **TAKES NO PARAMETERS**

#### Sample Request
```shell
$ curl 'http://localhost:5000/categories/2/questions'
```

#### Sample Response
```json
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```


### POST `/quizzes`
* Gets a random question for a TRIVIA quiz
* If all the questions are in the `previous_questions` list, it returns a `422` error.
* **BODY DETAILS:**

|key               |description                                   |required|
|------------------|----------------------------------------------|--------|
|quiz_category     |an object including category data `{id, type}`|true    |
|previous_questions|a list of ids of excluded questions           |false   |

#### Sample Request
```shell
$ curl -X POST 'http://localhost:5000/quizzes'
```

#### Sample Response
```json
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}
```