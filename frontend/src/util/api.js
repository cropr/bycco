const openapi = {
    "openapi": "3.0.2",
    "info": {
        "title": "Bycco",
        "description": "Belgisch jeugd",
        "version": "0.0.1"
    },
    "paths": {
        "/api/pages": {
            "get": {
                "summary": "Api Get Pages", "operationId": "get_pages", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/PageListOut" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/a/pages": {
            "get": {
                "summary": "Api Anon Get Pages", "operationId": "anon_get_pages", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/PageListOut" } } } } }
            }
        },
        "/api/pages/backup": {
            "post": {
                "summary": "Api Backup Pages", "operationId": "backup_pages", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "title": "Response Api Backup Pages Api Pages Backup Post", "type": "array", "items": { "$ref": "#/components/schemas/PageOptional" } } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/pages/restore": {
            "post": {
                "summary": "Api Restore Pages", "operationId": "restore_pages", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/PageListOut" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/page": {
            "post": {
                "summary": "Api Add Page", "operationId": "add_page", "requestBody": { "content": { "application/json": { "schema": { "$ref": "#/components/schemas/PageIn" } } }, "required": true }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "title": "Response Api Add Page Api Page Post", "type": "string" } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/page/{id}": {
            "get": {
                "summary": "Api Get Page", "operationId": "get_page", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            },
            "put": {
                "summary": "Api Update Page", "operationId": "update_page", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "requestBody": { "content": { "application/json": { "schema": { "$ref": "#/components/schemas/PageUpdate" } } }, "required": true }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            },
            "delete": {
                "summary": "Api Delete Page", "operationId": "delete_page", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/a/page/{id}": {
            "get": {
                "summary": "Api Anon Get Page", "operationId": "anon_get_page", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }
            }
        },
        "/api/a/routingtable": {
            "get": {
                "summary": "Api Anon Routingtable", "operationId": "anon_routingtable", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/RoutingTableListOut" } } } } }
            }
        },
        "/api/a/slug/{slug}": {
            "get": {
                "summary": "Api Anon Slug Page", "operationId": "anon_slug_page", "parameters": [{ "required": true, "schema": { "title": "Slug", "type": "string" }, "name": "slug", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }
            }
        },
        "/api/a/articles": {
            "get": {
                "summary": "Api Anon Get Articles", "operationId": "anon_get_articles", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } } }
            }
        },
        "/api/account": {
            "get": {
                "summary": "Api Get Accounts", "operationId": "get_accounts", "requestBody": { "content": { "application/json": { "schema": { "title": "Options", "type": "object", "default": {} } } } }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/AccountListOut" } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            },
            "post": {
                "summary": "Api Add Account", "operationId": "add_account", "requestBody": { "content": { "application/json": { "schema": { "$ref": "#/components/schemas/AccountIn" } } }, "required": true }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "title": "Response Api Add Account Api Account Post", "type": "string" } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/account/{id}": {
            "get": {
                "summary": "Api Get Account", "operationId": "get_account", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/AccountDetailedOut" } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            },
            "put": {
                "summary": "Api Update Account", "operationId": "update_account", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "requestBody": { "content": { "application/json": { "schema": { "$ref": "#/components/schemas/AccountDetailedIn" } } }, "required": true }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            },
            "delete": {
                "summary": "Api Delete Account", "operationId": "delete_account", "parameters": [{ "required": true, "schema": { "title": "Id", "type": "string" }, "name": "id", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": {} } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }, "security": [{ "HTTPBearer": [] }]
            }
        },
        "/api/login": {
            "post": {
                "summary": "Api Login", "operationId": "login", "requestBody": { "content": { "application/json": { "schema": { "$ref": "#/components/schemas/LoginIn" } } }, "required": true }, "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { "title": "Response Api Login Api Login Post", "type": "string" } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }
            }
        },
        "/api": {
            "get": {
                "summary": "Api Root", "operationId": "root", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { } } } } }
            }
        },
        "/": {
            "get": {
                "summary": "Htmlroot", "operationId": "htmlroot__get", "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { } } } } }
            }
        },
        "/page{path}": {
            "get": {
                "summary": "Htmlpage", "operationId": "htmlpage_page_path__get", "parameters": [{ "required": true, "schema": { "title": "Path", "type": "string" }, "name": "path", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }
            }
        },
        "/mgmt{path}": {
            "get": {
                "summary": "Htmlmgmt", "operationId": "htmlmgmt_mgmt_path__get", "parameters": [{ "required": true, "schema": { "title": "Path", "type": "string" }, "name": "path", "in": "path" }], "responses": { "200": { "description": "Successful Response", "content": { "application/json": { "schema": { } } } }, "422": { "description": "Validation Error", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/HTTPValidationError" } } } } }
            }
        }
    },
    "components": {
        "schemas": {
            "AccountDetailedIn": {
                "title": "AccountDetailedIn", "type": "object", "properties": { "domain": { "title": "Domain", "type": "string" }, "enabled": { "title": "Enabled", "type": "boolean" }, "first_name": { "title": "First Name", "type": "string" }, "last_name": { "title": "Last Name", "type": "string" }, "locale": { "title": "Locale", "type": "string" }, "logintype": { "$ref": "#/components/schemas/LoginType" }, "xtra": { "title": "Xtra", "type": "object" } }, "description": "contains the fields to update"
            },
            "AccountDetailedOut": {
                "title": "AccountDetailedOut", "required": ["email", "first_name", "id", "last_name", "logintype"], "type": "object", "properties": { "domain": { "title": "Domain", "type": "string", "default": "" }, "email": { "title": "Email", "type": "string" }, "email_verified": { "title": "Email Verified", "type": "boolean", "default": false }, "enabled": { "title": "Enabled", "type": "boolean", "default": false }, "first_name": { "title": "First Name", "type": "string" }, "id": { "title": "Id", "type": "string" }, "last_name": { "title": "Last Name", "type": "string" }, "locale": { "title": "Locale", "type": "string", "default": "" }, "logintype": { "$ref": "#/components/schemas/LoginType" }, "password_expiration_time": { "title": "Password Expiration Time", "type": "string", "format": "date-time" }, "xtra": { "title": "Xtra", "type": "object", "default": { } } }, "description": "An detailed view of a page "
            },
            "AccountIn": {
                "title": "AccountIn", "required": ["logintype", "id"], "type": "object", "properties": { "enabled": { "title": "Enabled", "type": "boolean", "default": false }, "logintype": { "$ref": "#/components/schemas/LoginType" }, "id": { "title": "Id", "type": "string" } }, "description": "contains the minimal fields  to create a new account"
            },
            "AccountListOut": {
                "title": "AccountListOut", "required": ["accounts"], "type": "object", "properties": { "accounts": { "title": "Accounts", "type": "array", "items": { "$ref": "#/components/schemas/AccountOut" } } }
            },
            "AccountOut": {
                "title": "AccountOut", "required": ["id"], "type": "object", "properties": { "id": { "title": "Id", "type": "string" } }, "description": "A readonly view used for listing pages, contains only the basic fields"
            },
            "CheckIdReply": {
                "title": "CheckIdReply", "required": ["belfound"], "type": "object", "properties": { "affiliated": { "title": "Affiliated", "type": "boolean" }, "belfound": { "title": "Belfound", "type": "boolean" }, "birthyear": { "title": "Birthyear", "type": "string" }, "first_name": { "title": "First Name", "type": "string", "default": "" }, "fidefound": { "title": "Fidefound", "type": "boolean", "default": false }, "idfide": { "title": "Idfide", "type": "string" }, "gender": { "$ref": "#/components/schemas/Gender" }, "last_name": { "title": "Last Name", "type": "string", "default": "" }, "nationality": { "title": "Nationality", "type": "string", "default": "BEL" }, "ratingbel": { "title": "Ratingbel", "type": "integer", "default": 0 }, "ratingfide": { "title": "Ratingfide", "type": "integer", "default": 0 }, "subfound": { "title": "Subfound", "type": "boolean", "default": false }, "subconfirmed": { "title": "Subconfirmed", "type": "boolean", "default": false }, "subid": { "title": "Subid", "type": "string" } }
            },
            "Gender": {
                "title": "Gender", "enum": ["M", "F"], "type": "string", "description": "An enumeration."
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError", "type": "object", "properties": { "detail": { "title": "Detail", "type": "array", "items": { "$ref": "#/components/schemas/ValidationError" } } }
            },
            "I18nField": {
                "title": "I18nField", "required": ["id", "name", "value"], "type": "object", "properties": { "id": { "title": "Id", "type": "string" }, "name": { "title": "Name", "type": "string" }, "value": { "title": "Value", "type": "string" } }, "description": "a subobject: contains a localised version of a field"
            },
            "LoginIn": {
                "title": "LoginIn", "required": ["logintype"], "type": "object", "properties": { "logintype": { "$ref": "#/components/schemas/LoginType" }, "password": { "title": "Password", "type": "string" }, "token": { "title": "Token", "type": "string" }, "username": { "title": "Username", "type": "string" } }
            },
            "LoginType": {
                "title": "LoginType", "enum": ["email", "facebook", "google"], "type": "string", "description": "An enumeration."
            },
            "PageOptional": {
                "title": "PageOptional", "type": "object", "properties": { "body": { "title": "Body", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "component": { "$ref": "#/components/schemas/PageComponent" }, "doctype": { "title": "Doctype", "type": "string" }, "enabled": { "title": "Enabled", "type": "boolean" }, "expirationdate": { "title": "Expirationdate", "type": "string" }, "intro": { "title": "Intro", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "name": { "title": "Name", "type": "string" }, "owner": { "title": "Owner", "type": "string" }, "publicationdate": { "title": "Publicationdate", "type": "string" }, "slug": { "title": "Slug", "type": "string" }, "title": { "title": "Title", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "creationtime": { "title": "Creationtime", "type": "string", "format": "date-time" }, "id": { "title": "Id", "type": "string" }, "modificationtime": { "title": "Modificationtime", "type": "string", "format": "date-time" } }, "description": "a Page with all fields Optional so we can work on raw database documents\nid and _id are boith provided for maximum flexibility"
            },
            "PageOut": {
                "title": "PageOut", "required": ["active", "creationtime", "doctype", "enabled", "id", "intro", "name", "modificationtime", "slug"], "type": "object", "properties": { "active": { "title": "Active", "type": "boolean" }, "creationtime": { "title": "Creationtime", "type": "string", "format": "date-time" }, "doctype": { "title": "Doctype", "type": "string" }, "enabled": { "title": "Enabled", "type": "boolean" }, "expirationdate": { "title": "Expirationdate", "type": "string" }, "id": { "title": "Id", "type": "string" }, "intro": { "title": "Intro", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "name": { "title": "Name", "type": "string" }, "modificationtime": { "title": "Modificationtime", "type": "string", "format": "date-time" }, "publicationdate": { "title": "Publicationdate", "type": "string" }, "slug": { "title": "Slug", "type": "string" } }, "description": "A readonly view used for listing pages, contains only the basic fields"
            },
            "PageUpdate": {
                "title": "PageUpdate", "type": "object", "properties": { "body": { "title": "Body", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "component": { "$ref": "#/components/schemas/PageComponent" }, "doctype": { "title": "Doctype", "type": "string" }, "enabled": { "title": "Enabled", "type": "boolean" }, "expirationdate": { "title": "Expirationdate", "type": "string" }, "intro": { "title": "Intro", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } }, "languages": { "title": "Languages", "type": "array", "items": { "type": "string" } }, "name": { "title": "Name", "type": "string" }, "owner": { "title": "Owner", "type": "string" }, "publicationdate": { "title": "Publicationdate", "type": "string" }, "slug": { "title": "Slug", "type": "string" }, "title": { "title": "Title", "type": "object", "additionalProperties": { "$ref": "#/components/schemas/I18nField" } } }, "description": "a Page"
            },
            "ValidationError": {
                "title": "ValidationError", "required": ["loc", "msg", "type"], "type": "object", "properties": { "loc": { "title": "Location", "type": "array", "items": { "type": "string" } }, "msg": { "title": "Message", "type": "string" }, "type": { "title": "Error Type", "type": "string" } }
            }
        },
        "securitySchemes": {
            "HTTPBearer": { "type": "http", "scheme": "bearer" }
        }
    }
};

export default openapi
