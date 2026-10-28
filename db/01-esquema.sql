-- Modelo de dados da Seção 2.4
CREATE TABLE usuario (
    id          uuid         PRIMARY KEY DEFAULT gen_random_uuid(),
    login       varchar(50)  NOT NULL UNIQUE
                CHECK (login = lower(login) AND position('@' in login) = 0),
    email       varchar(254) NOT NULL UNIQUE CHECK (email = lower(email)),
    nome        varchar(120) NOT NULL,
    hash_senha  varchar(255) NOT NULL
);
