% Zahra
% plot behavior (ROE, licks) of animals in SST experiment
% early days
% assumes that behavior is aligned to Fall.mat
% NOTE: day 1 of experiment should not have any behavior data aligned (no
% VR file, but there is a clampex file)

clear all; close all;
src = 'Y:\sstcre_analysis\fmats'; 
fls = dir(fullfile(src, "e*day*Fall.mat"));
grayColor = [.7 .7 .7];

for fl=1:numel(fls)
    flnm = fullfile(fls(fl).folder, fls(fl).name);
    mouse=load(flnm);
    try % don't plot if no behavior data aligned
        tr = mouse.rewards;
    end
    if exist('tr', 'var')==1
        sol = mouse.rewards==0.5; % codes for solenoid
        rew = mouse.rewards>0.5; % codes for single or double rewards
%         figure;
%         plot(sol*50, 'g', 'LineWidth',3); hold on; 
%         plot(rew*50, 'b', 'LineWidth',3); hold on; 
%         plot(mouse.lickVoltage*1000,'r'); hold on;
%         plot(mouse.forwardvel, 'Color', grayColor)
%         mousenm = flnm(26:29); day = str2num(flnm(34:36));
%         title(sprintf("mouse %s, day %i", mousenm, day))
%         xticks(1:1000:numel(mouse.ybinned))
%         xticklabels(ceil(mouse.timedFF(1:1000:end))) % plots in seconds
%         xlabel("time (s)")
%         ylabel("normalized value")
%         legend(["solenoid (CS)", "rewards", "lickvoltage", "forward velocity"])
    end
    mice{fl}=mouse;
    clear tr %remove condition from previous loop run
end

% average velocity of mouse e200
% days 2-5 = 3.6071
% days 8-14 = 14.6167
forwardvel=zeros(1,40000*7);
for i=10:16
    if i==10
        forwardvel = mice{i}.forwardvel;
    else
        forwardvel = [forwardvel mice{i}.forwardvel];
    end    
end
avvel_1 = mean(forwardvel);
% e201, days 10-16 = 13.18
forwardvel=zeros(1,40000*7);
for i=25:31
    if i==25
        forwardvel = mice{i}.forwardvel;
    else
        forwardvel = [forwardvel mice{i}.forwardvel];
    end    
end
avvel_2 = mean(forwardvel);


% plot mean image per day
% e200: i=1:16; e201: 17:31
j = 16; %offset
figure;
for i=17:31
    axes{i-j}=subplot(4,4,i-j);
    imagesc(mice{i}.ops.meanImg) %meanImg or max_proj
    colormap('gray')
    title(sprintf("day %i", i-j))
    axis off;
    hold on;    
    disp(i-j)
    disp(mice{i}.ops.save_path0)
end
linkaxes([axes{:}], 'xy')