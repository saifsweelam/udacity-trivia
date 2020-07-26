import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO:DONE
    Set up CORS.
    '''
    #   CORS(app)
    cors = CORS(app)

    '''
    @TODO: DONE
    Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    def paginate(result, page):
        start = QUESTIONS_PER_PAGE*(page-1)
        return result[start:start+QUESTIONS_PER_PAGE]

    '''
    @TODO: DONE
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = [category.format()
                          for category in Category.query.all()]
            return jsonify({
                'success': True,
                "categories": categories
            })
        except:
            abort(500)

    '''
    @TODO: DONE
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, int)
        try:
            total_questions = [question.format()
                               for question in Question.query.all()]
            questions = paginate(total_questions, page)
        except:
            abort(500)
        if not len(questions):
            abort(404)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(total_questions),
            'categories':
                [category.format() for category in Category.query.all()],
            'current_category': 'ALL'
        })

    '''
    @TODO: DONE
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
        except:
            abort(500)
        if not question:
            return abort(404)
        else:
            try:
                question.delete()
            except:
                abort(500)
        return jsonify({
            'success': True,
            'question_id': question.id
        })

    '''
    @TODO: DONE
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of
    the last page of the questions list in the "List" tab.
    '''

    '''
    @TODO: DONE
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def post_questions():
        data = request.get_json()
        if 'searchTerm' in data:
            try:
                search_term = data['searchTerm']
                questions = Question.query.filter(
                    Question.question.ilike('%{}%'.format(search_term))).all()
                return jsonify({
                    'success': True,
                    'questions': [question.format() for question in questions],
                    'total_questions': len(questions),
                    'current_category': 'Search'
                })
            except Exception as e:
                print(e)
                abort(500)
        else:
            if not (data['question'] and data['answer'] and
                    data['category'] and data['difficulty']):
                return abort(400)
            if not Category.query.get(data['category']):
                return abort(400)
            try:
                question = Question(
                    question=data['question'],
                    answer=data['answer'],
                    category=data['category'],
                    difficulty=data['difficulty']
                )
                question.insert()
                return jsonify({
                    'success': True,
                    'question': question.format()
                })
            except Exception as e:
                print(e)
                abort(500)

    '''
    @TODO: DONE
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
        except:
            print(e)
            abort(500)
        if not category:
            return abort(404)
        try:
            questions = [
                question.format() for question
                in Question.query.filter_by(category=category_id).all()
            ]
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category.type
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: DONE
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def quiz_question():
        data = request.get_json()
        if not (data['quiz_category']['id']):
            abort(400)
        category_id = data['quiz_category']['id']
        previous_questions = data['previous_questions'] if data[
            'previous_questions'] else []
        if category_id != 0 and not Category.query.get(category_id):
            abort(404)
        try:
            question_data = Question.query.all(
            )if category_id == 0 else Question.query.filter_by(
                category=category_id).all()
        except:
            abort(500)
        questions = [question.format() for question in question_data]
        questions = list(
            filter(lambda x: x['id'] not in previous_questions, questions))
        if len(questions) == 0:
            abort(422)
        question = random.choice(questions)
        return jsonify({
            'success': True,
            'question': question
        })

    '''
    @TODO: DONE
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def throw_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Resource Not Found',
            'status_code': 404
        }), 404

    @app.errorhandler(400)
    def throw_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Bad Request',
            'status_code': 400
        }), 400

    @app.errorhandler(500)
    def throw_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Internal Server Error',
            'status_code': 500
        }), 500

    @app.errorhandler(422)
    def throw_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Unprocessable',
            'status_code': 422
        }), 422

    @app.errorhandler(405)
    def throw_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Method Not Allowed',
            'status_code': 405
        }), 405

    return app
