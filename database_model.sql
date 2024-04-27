/*
    Stores the user contact list, containing their name, number and optionally, email.
    Name and number are required
*/
CREATE TABLE contacts (
    contact_id      INT                 IDENTITY(1, 1),
    contact_name    VARCHAR(42)         NOT NULL,
    contact_number  VARCHAR(18)         NOT NULL,
    contact_email   VARCHAR(40)         NULL

    CONSTRAINT      contact_id_pk       PRIMARY KEY(contact_id),
    CONSTRAINT      contact_number_un   UNIQUE(contact_number)
)

/*
    Stores the text models for the pre-made texts
    If a name is not inserted, it gives a Default name containing it's Id.
*/
CREATE TABLE text_models(
    text_id         INT                 IDENTITY(1, 1),
    text_name       VARCHAR(50)         NULL,
    model_text      TEXT                NOT NULL

    CONSTRAINT      text_id_pk          PRIMARY KEY(text_id),
    CONSTRAINT      text_name_un        UNIQUE(text_name),
    CONSTRAINT      text_name_df        DEFAULT('Model ' + CAST(IDENT_CURRENT('text_models') AS VARCHAR(10)))
)