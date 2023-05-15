insert into subject(id, name, creator) values (1, 'Mathematik 1', 1);
insert into subject(id, name, creator) values (2, 'Mathematik 2', 1);
insert into subject(id, name, creator) values (3, 'Programmieren 1', 1);
insert into subject(id, name, creator) values (4, 'Programmieren 2', 1);
insert into subject(id, name, creator) values (5, 'Datenbanken', 1);

insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (1, 'Was macht a in der folgen Funktion? a*sin(b * x + c) + d?', 'Streckung/Stauchung in y-Achse', 1, 1, 24, 12);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (2, 'Wie lautet die Ableitung von ln(x)?', '1/x', 1, 1 ,12, 18);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (3, 'Was ist das unbestimmte Integral für cosh(x))?', 'sinh(x)+c', 2, 1 ,0, 0);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (4, 'Wie rechnet man Polarkoordinaten in rechtwinklige Kooridnaten um?', 'a=r*cos(phi), b=r*sin(phi)', 2, 1 ,0, 0);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (5, 'Kann eine Klasse in Java mehrere Interfaces Implementieren?', 'Ja, nicht aber Mehrfachvererbung', 3, 1 ,101, 99);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (6, 'Welche Werte deckt der Datentyp byte ab in Java?', '-128 bis 127?', 3, 1 ,420, 1337);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (7, 'Was macht Reflection?', 'Reflection erlaubt dem Programm sich selbst zu untersuchen und zu modifizieren', 4, 1 ,0, 44);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (8, 'Was ist eine synchronized Methode?', 'Eine Methode in der zu jedem Zeitpunkt nur ein Thread sein darf.', 4, 1 ,0 , 123);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (9, 'Was ist die DDL', 'Data Definition Language?', 5, 1 ,11, 0);
insert into questions(id, question, answer, subject, creator, count_correct, count_wrong) values (10, 'Was ist die DML', 'Data Manipulation Language?', 5, 1 ,0, 0);

delete from user;
delete from subject;
delete from questions;