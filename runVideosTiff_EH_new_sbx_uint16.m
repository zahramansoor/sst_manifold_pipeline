%runVideos
%210103 EH. "loadVideoTiffNoSplit_EH2_new_sbx_uint16" for non-suite2p analy
%doesn't do weird divide by two to decrease max values.
%200820 EH. points to "loadVideoTiffNoSplit_EH2_new_sbx" for new sbx form.
%bi offsets different in new scanbox and sbx files also changed
% 200329 EH. modified from moi's code
% 200501 EH, make 'bi new' default
% also stopped removing last 4 from files{f} to make compatible with
% loadVideoTiffNoSplit_EH2.
% calls "loadVideoTiffNoSplit_EH2". see that file for changes
% changes loading, processing, and saving of tif files for suite2p

%Allows you to select multiple sbx files, splits out planes to tifs.
clear all; close all;
%ZD added for her computer on 20230215
javaaddpath 'C:\Program Files\MATLAB\R2021b\java\mij.jar'
javaaddpath 'C:\Program Files\MATLAB\R2021b\java\ij.jar'

num_files=input('Enter number of files to run:');
% Fs=input('Frame Rate? ');
% num_files=1;
files{num_files}=0;
paths{num_files}=0;
scan_type{num_files}=0;
for f=1:num_files
    [files{f},paths{f}]=uigetfile('*.sbx','pick your files');
%     [name,paths{f}]=uigetfile('*.sbx','pick your files');
%     files{f}=name(1:end-4);
%     scan_type{f}=input('Enter type of scanning (uni,bi,uni new,bi new): ');
    scan_type{f}='bi new';
    cd (paths{f}); %set path
end
% Fs=31;
%Send sbx files to be split into a mat file for each plane
for f=1:num_files
%     loadVideoTiff(paths{f},files{f},num_planes(f),Fs);
    loadVideoTiffNoSplit_EH2_new_sbx_uint16(paths{f},files{f},scan_type{f});
end




