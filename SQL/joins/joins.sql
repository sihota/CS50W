CREATE TABLE passengers
(
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  flight_id INTEGER REFERENCES flights
);

INSERT INTO passengers (name, flight_id) VALUES ('Alice', 1);
INSERT INTO passengers (name, flight_id) VALUES ('Bob', 1);
INSERT INTO passengers (name, flight_id) VALUES ('Charlie', 2);
INSERT INTO passengers (name, flight_id) VALUES ('Dave', 2);
INSERT INTO passengers (name, flight_id) VALUES ('Erin', 4);
INSERT INTO passengers (name, flight_id) VALUES ('Frank', 6);
INSERT INTO passengers (name, flight_id) VALUES ('Grace', 6);
SELECT * FROM flights WHERE id IN
  (
    SELECT flight_id FROM passengers GROUP BY flight_id HAVING COUNT(*) > 1
  );
