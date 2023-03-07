USE sst_zahra;

CREATE TABLE mice (name VARCHAR(20) PRIMARY KEY, type VARCHAR(1000) NOT NULL, 
surgeon VARCHAR(20) NOT NULL, surgery_date DATE, first_imaging_session DATE NOT NULL);

CREATE TABLE two_photon (mouse_name VARCHAR(20), session_id DATE, PRIMARY KEY (mouse_name, session_id), week INT, raw_data VARCHAR(1000), processed_data VARCHAR(1000), 
manual_inspect_done BOOLEAN, use_for_analysis BOOLEAN, notes VARCHAR(10000));

CREATE TABLE behavior (mouse_name VARCHAR(20) PRIMARY KEY, session_iid DATE REFERENCES two_photon(session_id) ON DELETE NO ACTION,
week INT, VR VARCHAR(1000), clampex VARCHAR(1000), aligned_to_images BOOLEAN);

CREATE TABLE camera (mouse_name VARCHAR(20) PRIMARY KEY, session_iiid DATE REFERENCES two_photon(session_id) ON DELETE NO ACTION,
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

######
# add data
INSERT INTO mice VALUES ('e200', 'SST-Cre with inhibitory opsin - GtACR2 (soma-targeted)', 'EH', NULL, '2023-02-14');
INSERT INTO mice VALUES ('e201', 'SST-Cre with inhibitory opsin - GtACR2 (soma-targeted)', 'EH', NULL, '2023-02-14');

INSERT INTO two_photon VALUES ('e200', '2023-02-14', 1, 'Z:\\sstcre_imaging\\e200\\1', 'Z:\\sstcre_imaging\\e200\\1', TRUE, FALSE, 'no behavior');
INSERT INTO two_photon VALUES ('e201', '2023-02-14', 1, 'Z:\\sstcre_imaging\\e201\\1', 'Z:\\sstcre_imaging\\e201\\1', TRUE, FALSE, 'no behavior');
INSERT INTO two_photon VALUES ('e201', '2023-02-13', 1, 'Z:\\sstcre_imaging\\e201\\0_ref_pln_day', NULL, TRUE, FALSE, 'ref plane and z stack, no behavior');
INSERT INTO two_photon VALUES ('e200', '2023-02-13', 1, 'Z:\\sstcre_imaging\\e200\\0_ref_pln_day', NULL, TRUE, FALSE, 'ref plane and z stack, no behavior');
INSERT INTO two_photon VALUES ('e200', '2023-02-15', 1, 'Z:\\sstcre_imaging\\e200\\2', 'Z:\\sstcre_imaging\\e200\\2', TRUE, TRUE, 'cameras not in trigger mode');
INSERT INTO two_photon VALUES ('e201', '2023-02-15', 1, 'Z:\\sstcre_imaging\\e201\\2', 'Z:\\sstcre_imaging\\e201\\2', TRUE, TRUE, 'cameras not in trigger mode');
INSERT INTO two_photon VALUES 
('e201', '2023-02-16', 1, 'Z:\\sstcre_imaging\\e201\\3', 'Z:\\sstcre_imaging\\e201\\3', TRUE, TRUE, ''),
('e200', '2023-02-16', 1, 'Z:\\sstcre_imaging\\e200\\3', 'Z:\\sstcre_imaging\\e200\\3', TRUE, TRUE, ''),
('e201', '2023-02-22', 2, 'Z:\\sstcre_imaging\\e201\\4', 'Z:\\sstcre_imaging\\e201\\4', TRUE, TRUE, ''),
('e200', '2023-02-22', 2, 'Z:\\sstcre_imaging\\e200\\4', 'Z:\\sstcre_imaging\\e200\\4', TRUE, FALSE, 'may want to drop day, dark images');

 