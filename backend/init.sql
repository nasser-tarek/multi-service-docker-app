CREATE TABLE IF NOT EXISTS visits (
    id SERIAL PRIMARY KEY,
    counter INT DEFAULT 0
);

-- Insert initial row
INSERT INTO visits (counter) VALUES (0);
