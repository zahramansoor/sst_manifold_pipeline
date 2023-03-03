CREATE TABLE mice (name VARCHAR(20) PRIMARY KEY, type VARCHAR(1000) NOT NULL, 
surgeon VARCHAR(20) NOT NULL, surgery_date DATE, first_imaging_session DATE NOT NULL);

CREATE TABLE two_photon (mouse_name VARCHAR(20) PRIMARY KEY, session DATE, week INT, raw_data VARCHAR(1000), processed_data VARCHAR(1000), 
manual_inspect_done BOOLEAN, use_for_analysis BOOLEAN, notes VARCHAR(10000));

CREATE TABLE behavior (mouse_name VARCHAR(20) PRIMARY KEY, session DATE, 
week INT, VR VARCHAR(1000), clampex VARCHAR(1000), aligned_to_images BOOLEAN);

CREATE TABLE camera (mouse_name VARCHAR(20) PRIMARY KEY, session DATE, 
week INT, eye VARCHAR(1000), tail VARCHAR(1000), trigger_on BOOLEAN, DLC BOOLEAN, pose_data VARCHAR(1000));

ALTER TABLE two_photon
ADD FOREIGN KEY(mouse_name)
REFERENCES mice(name)
ON DELETE CASCADE;

ALTER TABLE behavior
ADD FOREIGN KEY(mouse_name)
REFERENCES mice(name)
ON DELETE CASCADE;

ALTER TABLE camera
ADD FOREIGN KEY(mouse_name)
REFERENCES mice(name)
ON DELETE CASCADE;

ALTER TABLE behavior
ADD FOREIGN KEY(session)
REFERENCES two_photon(session)
ON DELETE CASCADE;
