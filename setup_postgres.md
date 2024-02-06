```bash
psql -U postgres
```

```bash
CREATE DATABASE mall;
\c mall;

CREATE TABLE items (
    id VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL,
    thumbnail VARCHAR(255),
    category VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
```
