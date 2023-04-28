insert into user(id, username, password) values (1, 'Lewin', 'GeheimesPasswort123');
insert into user(id, username, password) values (2, 'nichtLewin', 'SicheresPasswort#');

insert into subject(id, name, creator) values (1, 'Mathematik 1', 1);
insert into subject(id, name, creator) values (2, 'Mathematik 2', 1);
insert into subject(id, name, creator) values (3, 'Programmieren 1', 2);
insert into subject(id, name, creator) values (4, 'Programmieren 2', 1);
insert into subject(id, name, creator) values (5, 'Datenbanken', 2);

insert into questions(id, question, answer, subject, creator) values (1, 'Was macht a in der folgen Funktion?\na*sin(b * x + c) + d?', 'Streckung/Stauchung in y-Achse', 1, 2);
insert into questions(id, question, answer, subject, creator) values (2, 'Wie lautet die Ableitung von ln(x)?', '1/x', 1, 2);
insert into questions(id, question, answer, subject, creator) values (3, 'Was ist das unbestimmte Integral für cosh(x))?', 'sinh(x)+c', 2, 2);
insert into questions(id, question, answer, subject, creator) values (4, 'Wie rechnet man Polarkoordinaten in rechtwinklige Kooridnaten um?', 'a=r*cos(phi), b=r*sin(phi)', 2, 2);
insert into questions(id, question, answer, subject, creator) values (5, 'Kann eine Klasse in Java mehrere Interfaces Implementieren?', 'Ja, nicht aber Mehrfachvererbung', 3, 1);
insert into questions(id, question, answer, subject, creator) values (6, 'Welche Werte deckt der Datentyp byte ab in Java?', '-128 bis 127?', 3, 1);
insert into questions(id, question, answer, subject, creator) values (7, 'Was macht Reflection?', 'Reflection erlaubt dem Programm sich selbst zu untersuchen und zu modifizieren', 4, 1);
insert into questions(id, question, answer, subject, creator) values (8, 'Was ist eine synchronized Methode?', 'Eine Methode in der zu jedem Zeitpunkt nur ein Thread sein darf.', 4, 1);
insert into questions(id, question, answer, subject, creator) values (9, 'Was ist die DDL', 'Data Definition Language?', 5, 1);
insert into questions(id, question, answer, subject, creator) values (10, 'Was ist die DML', 'Data Manipulation Language?', 5, 1);

delete from user;
delete from subject;
delete from questions;