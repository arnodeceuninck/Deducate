# from flask_mail import Message
# from flask import render_template
# from app import mail, app
# from threading import Thread
#
#
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     Thread(target=send_async_email, args=(app, msg)).start()
#
#
# def send_mentor_email(future_student, richting, emails):
#     send_email("[Educate] We found a match", sender=app.config["ADMINS"][0], recipients=[emails],
#                text_body=render_template('emails/mentor_email.txt', future_student=future_student.name,
#                                          emails=future_student.emails, richting=richting),
#                html_body=render_template('emails/mentor_email.html', future_student=future_student.name,
#                                          emails=future_student.emails, richting=richting))
#
#
# def send_future_student_email(mentor, richting, emails):
#     send_email("[Educate] We found someone who can help you", sender=app.config["ADMINS"][0], recipients=[emails],
#                text_body=render_template('emails/future_student_email.txt', mentor=mentor.name, emails=mentor.emails,
#                                          richting=richting),
#                html_body=render_template('emails/future_student_email.html', mentor=mentor.name, emails=mentor.emails,
#                                          richting=richting))
