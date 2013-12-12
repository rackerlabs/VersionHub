-- Model Author: Kacie Houser - Hussam Dawood - Roger Enriquez

SET check_function_bodies = false;

DROP DATABASE version_hub;
-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: version_hub | type: DATABASE --
CREATE DATABASE version_hub;

SET search_path TO pg_catalog,public;

CREATE USER version_hub_user WITH PASSWORD 'Eur0pa42!';

\c version_hub;

-- object: public.applications | type: TABLE --
CREATE TABLE public.applications(
	id serial NOT NULL,
	name varchar(1024) NOT NULL,
	description text,
	github varchar(512),
	contact_email varchar(512) NOT NULL,
	CONSTRAINT pk_applications PRIMARY KEY (id)

);

-- object: public.environments | type: TABLE --
CREATE TABLE public.environments(
	id serial NOT NULL,
	application integer NOT NULL,
	environment_type integer NOT NULL,
	endpoint varchar(512),
	CONSTRAINT pk_environments PRIMARY KEY (id)
);

-- object: public.environment_types | type: TABLE --
CREATE TABLE public.environment_types(
	id serial NOT NULL,
	label varchar(512),
	CONSTRAINT pk_environment_types PRIMARY KEY (id)
);

-- object: public.envoirnment_dependencies_xref | type: TABLE --
CREATE TABLE public.environment_dependencies_xref(
	environment integer NOT NULL,
	dependency integer NOT NULL,
	CONSTRAINT pk_environment_dependencies_xref PRIMARY KEY (environment, dependency)
);

-- object: public.version_logs | type: TABLE --
CREATE TABLE public.version_logs(
	id serial NOT NULL,
	version integer NOT NULL,
	dependency_data text[3] NOT NULL, --version, environment type, application name
	CONSTRAINT pk_version_log PRIMARY KEY (id)
);

-- object: public.versions | type: TABLE --
CREATE TABLE public.versions(
	id serial NOT NULL,
	environment integer NOT NULL,
	version varchar(32),
	date_created timestamp DEFAULT NOW(),
	CONSTRAINT pk_versions PRIMARY KEY (id)

);

-- object: public.notifications | type: TABLE --
CREATE TABLE public.notifications(
	id serial NOT NULL,
	environment integer NOT NULL,
	message text NOT NULL,
	date_created timestamp DEFAULT NOW(),
	read boolean DEFAULT false,
	CONSTRAINT pk_notifications PRIMARY KEY (id)

);


-- object: fk_version_version_logs | type: CONSTRAINT --
ALTER TABLE public.version_logs ADD CONSTRAINT fk_version_version_logs FOREIGN KEY (version)
REFERENCES public.versions (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_environment_notifications | type: CONSTRAINT --
ALTER TABLE public.notifications ADD CONSTRAINT fk_environment_notifications FOREIGN KEY (environment)
REFERENCES public.environments (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_environment_versions | type: CONSTRAINT --
ALTER TABLE public.versions ADD CONSTRAINT fk_environment_versions FOREIGN KEY (environment)
REFERENCES public.environments (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_application_environments | type: CONSTRAINT --
ALTER TABLE public.environments ADD CONSTRAINT fk_application_environments FOREIGN KEY (application)
REFERENCES public.applications (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_environment_type_environments | type: CONSTRAINT --
ALTER TABLE public.environments ADD CONSTRAINT fk_environment_type_environments FOREIGN KEY (environment_type)
REFERENCES public.environment_types (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_environment_environments | type: CONSTRAINT --
ALTER TABLE public.environment_dependencies_xref ADD CONSTRAINT fk_environment_environments FOREIGN KEY (environment)
REFERENCES public.environments (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


-- object: fk_dependency_environments | type: CONSTRAINT --
ALTER TABLE public.environment_dependencies_xref ADD CONSTRAINT fk_dependency_applications FOREIGN KEY (dependency)
REFERENCES public.environments (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION NOT DEFERRABLE;


--Test Data
INSERT INTO applications (name, description, github, contact_email) VALUES('Cloud Control', 'An app for all apps', '', 'phteven@email.com');
INSERT INTO applications (name, description, github, contact_email) VALUES('Nova', 'Super Cloud Awesomenessess', '', 'dev_null@email.com');
INSERT INTO applications (name, description, github, contact_email) VALUES('LBaaS', 'Load Balancing Goodness', '', 'dev_null@email.com');

INSERT INTO environment_types (label) VALUES('Staging');
INSERT INTO environment_types (label) VALUES('Production');

INSERT INTO environments (application, environment_type) VALUES(
	(SELECT id FROM applications WHERE name = 'Cloud Control'), 
	(SELECT id FROM environment_types WHERE label = 'Staging'));

INSERT INTO environments (application, environment_type) VALUES(
	(SELECT id FROM applications WHERE name = 'Nova'),
	(SELECT id FROM environment_types WHERE label = 'Staging'));

INSERT INTO environments (application, environment_type) VALUES(
	(SELECT id FROM applications WHERE name = 'LBaaS'),
	(SELECT id FROM environment_types WHERE label = 'Staging'));

INSERT INTO environment_dependencies_xref (environment, dependency) VALUES(
	(SELECT id FROM applications WHERE name = 'Cloud Control'),
	(SELECT id FROM applications WHERE name = 'Nova'));

INSERT INTO environment_dependencies_xref (environment, dependency) VALUES(
	(SELECT id FROM applications WHERE name = 'Cloud Control'),
	(SELECT id FROM applications WHERE name = 'LBaaS'));

-- Views
        SELECT
                a2.name        as environment_name,
                a1.name        as dependency_name,
                et.label       as environment_type,
                e.id           as environment_id,
                ex.dependency  as dependency_id
        FROM
                environments e
        JOIN environment_dependencies_xref ex ON ex.environment = e.id
        JOIN applications a1 ON a1.id = ex.dependency
        JOIN applications a2 ON a2.id = ex.environment
        JOIN environment_types et ON et.id = e.environment_type;


CREATE OR REPLACE VIEW environment_notifications AS
	SELECT 
		n.message 		as notification_message,
		n.date_created 	as created_on,
		e.id 			as environment_id
	FROM
		notifications n 
	JOIN 
		environments e ON e.id = n.environment;


CREATE OR REPLACE VIEW environment_version_log AS
	SELECT
	 	v.id 		as version_id,
	 	v.version 	as version_text,
	 	e.id 		as environment_id
	FROM 
		versions v
	JOIN environments e ON e.id = v.environment
	ORDER BY v.date_created DESC;


CREATE OR REPLACE VIEW get_applications AS
	SELECT 
		a.id, 
		a.name, 
		(
			SELECT 
				n.id 
			FROM 
				notifications n 
			JOIN environments e ON e.id = n.environment
			JOIN applications a2 ON a2.id = e.application
			WHERE 
				n.read = false 
			AND 
				a2.id = a.id  
			AND
				environment_type = (SELECT 
										id 
									FROM 
										environment_types
									WHERE label = 'Staging') LIMIT 1)
		AS staging,
		(
			SELECT 
				n.id 
			FROM 
				notifications n 
			JOIN environments e ON e.id = n.environment
			JOIN applications a2 ON a2.id = e.application
			WHERE 
				n.read = false 
			AND 
				a2.id = a.id  
			AND
				environment_type = (SELECT 
										id 
									FROM 
										environment_types
									WHERE label = 'Production') LIMIT 1)
		AS production
		FROM 
			applications a
		ORDER BY a.name;

-- Procedures
CREATE TYPE application_notification AS (application_id int, application_name varchar(1024), staging int, production int);

CREATE OR REPLACE FUNCTION get_environment_types()
RETURNS setof environment_types AS 
	$$ 
		SELECT * FROM environment_types;
	$$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_all_applications()
RETURNS setof application_notification AS 
	$$ 
		SELECT * FROM get_applications;
	$$
LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_application(int)
RETURNS setof applications AS 
	$$ 
		SELECT * FROM applications WHERE id = $1;
	$$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION create_application(name_text varchar(1024), description_text text, github_text varchar(512), contact_email_text varchar(512))
RETURNS int AS
	$$ 
		BEGIN
			INSERT INTO applications (name, description, github, contact_email) VALUES (name_text, description_text, github_text, contact_email_text);
			RETURN currval('applications_id_seq');
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_application(application_id int, name_text varchar(1024), description_text text, github_text varchar(512), contact_email_text varchar(512))
RETURNS VOID AS
	$$ 
		BEGIN
			UPDATE 
				applications 
			SET 
				name = name_text,
				description = description_text,
				github = github_text,
				contact_email= contact_email_text
			 WHERE 
			 	id = application_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_application(application_id int) 
RETURNS VOID AS
	$$ 
		BEGIN
			DELETE FROM applications WHERE id = application_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_environment(application_id int, environment_type_id int, endpoint_text varchar(512))
RETURNS VOID AS
	$$ 
		BEGIN
			INSERT INTO environments (application, environment_type, endpoint) VALUES (application_id, environment_type_id, endpoint_text);
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_environment(environment_id int, endpoint_text varchar(512))
RETURNS VOID AS
	$$ 
		BEGIN
			UPDATE environments SET endpoint = endpoint_text WHERE id = environment_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_environment(environment_id int) 
RETURNS VOID AS
	$$ 
		BEGIN
			DELETE FROM environments WHERE id = environment_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_dependency(environment_id int, dependency_id int)
RETURNS VOID AS
	$$ 
		BEGIN
			INSERT INTO environment_dependencies_xref (environment, dependency) VALUES (environment_id, dependency_id);
		END
	$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_dependency(environment_id int, dependency_id int) 
RETURNS VOID AS
	$$ 
		BEGIN
			DELETE FROM environment_dependencies_xref WHERE environment = environment_id AND dependency = dependency_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_version(environment_id int, version_text varchar(32))
RETURNS int AS
	$$ 
		BEGIN
			INSERT INTO versions (environment, version) VALUES (environment_id, version_text);
			RETURN currval('versions_id_seq');
		END
	$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_version(version_id int) 
RETURNS VOID AS
	$$ 
		BEGIN
			DELETE FROM versions WHERE id = version_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION set_notification_read(notification_id int)
RETURNS VOID AS
	$$ 
		BEGIN
			UPDATE notifications SET read = TRUE WHERE id = notification_id;
		END
	$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_environment_dependencies(int)
RETURNS setof environment_dependencies AS
	$$ 
		SELECT * FROM environment_dependencies WHERE environment_id = $1;
	$$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_environment_noifications(int)
RETURNS setof environment_notifications AS
	$$ 
		SELECT * FROM environment_notifications WHERE environment_id = $1 AND read = FALSE;
	$$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_environment_version_log(int)
RETURNS setof environment_version_log AS
	$$ 
		SELECT * FROM environment_version_log WHERE environment_id = $1;
	$$
LANGUAGE sql;


CREATE OR REPLACE FUNCTION get_dependency_version_log(int)
RETURNS setof version_logs AS
	$$ 
		SELECT * FROM version_logs WHERE version = $1;
	$$
LANGUAGE sql;


-- Trigger Functions
CREATE OR REPLACE FUNCTION update_version_logs() RETURNS TRIGGER AS $version_log_update$
    DECLARE
        dependent_id INTEGER;
		dep_info RECORD;
    
    BEGIN
        FOR dependent_id IN
        	SELECT dependency FROM environment_dependencies_xref WHERE environment = NEW.environment
        LOOP
        	SELECT 
        		v.version as version,
        		a.name as name,
        		et.label as env
        	INTO dep_info 
        	FROM versions v
        	JOIN environments e ON e.id = v.environment
        	JOIN applications a ON a.id = e.application
        	JOIN environment_types et ON et.id = e.environment_type
        	WHERE environment = dependent_id ORDER BY date_created DESC LIMIT 1;

        	IF dep_info.version IS NOT NULL THEN
	        	INSERT INTO 
	        		version_logs (version, dependency_data) 
	        	VALUES
	        		(NEW.id, ARRAY[dep_info.version, dep_info.name, dep_info.env]);
	        END IF;

        END LOOP;

        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$version_log_update$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_dependent_notifications() RETURNS TRIGGER AS $notification_update$
    DECLARE
        dependent_id INTEGER;
    	dependent_name VARCHAR(1024);
    BEGIN
        FOR dependent_id IN
        	SELECT environment FROM environment_dependencies_xref WHERE dependency = NEW.environment
        LOOP
        	SELECT 
        		a.name 
        	INTO dependent_name
        	FROM 
        		applications a 
        	JOIN environments e ON e.application = a.id 
        	WHERE 
        		e.id = NEW.environment;

        	INSERT INTO 
        		notifications (environment, message, date_created) 
        	VALUES
        		(dependent_id, dependent_name || ' has moved to version ' || NEW.version, current_timestamp);

        END LOOP;

        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$notification_update$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER version_log_update
    AFTER INSERT ON versions
    FOR EACH ROW
    EXECUTE PROCEDURE update_version_logs();

CREATE TRIGGER notification_update
    AFTER INSERT ON versions
    FOR EACH ROW
    EXECUTE PROCEDURE update_dependent_notifications(environment);

--INSERT INTO versions (environment, version, date_created) values (2, '1.0', current_timestamp)

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO version_hub_user;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA PUBLIC TO version_hub_user;

