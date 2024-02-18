CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users_audit (
    audit_id SERIAL PRIMARY KEY,
    user_id INT,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    operation VARCHAR(50)
);

CREATE OR REPLACE FUNCTION log_user_update()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO users_audit(user_id, operation)
        VALUES (NEW.user_id, TG_OP);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO users_audit(user_id, operation)
        VALUES (NEW.user_id, TG_OP);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO users_audit(user_id, operation)
        VALUES (OLD.user_id, TG_OP);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION log_user_update();