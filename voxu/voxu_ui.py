from flask import Blueprint, render_template, current_app
import openai
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from .database import DatabaseConfigurator
from .models import get_http_request_log_table_class

voxu_blueprint = Blueprint('voxu', __name__, url_prefix='/voxu', template_folder='templates')


@voxu_blueprint.route('/logs')
def logs():
    HTTPRequestLog = get_http_request_log_table_class()
    db_session = DatabaseConfigurator(current_app).init_db()
    logs = db_session.query(HTTPRequestLog).all()
    db_session.close()
    return render_template('logs.html', logs=logs)


@voxu_blueprint.route('/log/<int:log_id>')
def get_log_solution_with_openai(log_id):
    HTTPRequestLog = get_http_request_log_table_class()
    db_session = DatabaseConfigurator(current_app).init_db()
    log = db_session.query(HTTPRequestLog).filter_by(id=log_id).first()
    if log:
        solution = get_openai_response(log)
        db_session.close()
        return solution
    else:
        return "Log not found"


def get_openai_response(log):
    openai.api_key = current_app.config.get('OPENAI_API_KEY')
    system_prompt = ("You are a helpful AI assistant that provides solutions to server problems."
                     "Your goal is to provide a solution to the problem described in the log."
                     "You are an expert in server troubleshooting and have access to a vast knowledge base."
                     "You MUST provide the solution in HTML format using just the following tags ONLY: <p>,<h4>, "
                     "<h5>, <ul>, <ol>, <li>, <a>, <code>, <pre>, <blockquote> <br>, <hr>."
                     "You must provide a solution that is clear, concise, and helpful to the user."
                     "The solution should be easy to understand."
                     "The solution cannot be harmful or malicious in any way."
                     "The solution should be relevant to the problem described in the log."
                     "Include any relevant information that will help the user understand the solution."
                     "Incase you are unable to provide a solution, please let the user know."
                     "You can start by saying 'Given the following log, provide a solution to the problem:'.")
    system_message = ChatCompletionSystemMessageParam(
        role="system",
        content=system_prompt,
    )
    user_message = ChatCompletionUserMessageParam(
        role="user",
        content=f"Given the following log, provide a solution to the problem:\n\n"
                f"Method: {log.method}\n"
                f"IP Address: {log.ip_address}\n"
                f"URL: {log.url}\n"
                f"Headers: {log.headers}\n"
                f"Body: {log.body}\n"
                f"Response Status: {log.response_status}\n"
                f"Response Headers: {log.response_headers}\n"
                f"Response Body: {log.response_body}\n"
                f"Timestamp: {log.timestamp}\n\n"
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message],
        timeout=120,
        temperature=0.5
    )
    return response.choices[0].message.content
