%Zahra
%run VR align

mouse_name = "e200";
days = 10:11;
src = "Z:\sstcre_imaging";
addpath(fullfile(pwd, "utils"));
for day=days
    daypth = dir(fullfile(src, mouse_name, string(day), "behavior", "vr\*.mat"));
    fmatfl = dir(fullfile(src, mouse_name, string(day), '**\Fall.mat')); 
    savepthfmat = VRalign(fullfile(daypth.folder, daypth.name),fullfile(fmatfl.folder, fmatfl.name));
    disp(savepthfmat)
end