
SELECT *
FROM tasks
WHERE user_id = 1;


SELECT *
FROM tasks
WHERE status_id = (
    SELECT id FROM status WHERE name = 'new'
);


UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;


SELECT fullname, email
FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id FROM tasks WHERE user_id IS NOT NULL
);


INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Learn SQL Basics',
    'Complete SQL exercises and practice joins.',
    (SELECT id FROM status WHERE name = 'new'),
    1
);


SELECT t.id, t.title, s.name AS status
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name != 'completed';


DELETE FROM tasks
WHERE id = 1;


SELECT *
FROM users
WHERE email LIKE '%@gmail.com';


UPDATE users
SET fullname = 'Updated User Name'
WHERE id = 1;


SELECT s.name AS status, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name
ORDER BY task_count DESC;


SELECT t.title, u.fullname, u.email
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

SELECT *
FROM tasks
WHERE description IS NULL OR description = '';


SELECT u.fullname, t.title, s.name AS status
FROM users u
JOIN tasks t ON u.id = t.user_id
JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';


SELECT u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.fullname
ORDER BY task_count DESC;
