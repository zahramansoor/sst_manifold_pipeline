% Zahra
% plot behavior (ROE, licks) of animals in SST experiment
% early days
% assumes that behavior is aligned to Fall.mat
% NOTE: day 1 of experiment should not have any behavior data aligned (no
% VR file, but there is a clampex file)

clear all; close all;
src = 'Y:\sstcre_analysis\fmats'; 
fls = dir(fullfile(src, "e*Fall.mat"));
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
        figure;
        plot(sol*50, 'g', 'LineWidth',3); hold on; 
        plot(rew*50, 'b', 'LineWidth',3); hold on; 
        plot(mouse.lickVoltage*1000,'r'); hold on;
        plot(mouse.forwardvel, 'Color', grayColor)
        mousenm = flnm(26:29); day = str2num(flnm(34:36));
        title(sprintf("mouse %s, day %i", mousenm, day))
        xticks(1:1000:numel(mouse.ybinned))
        xticklabels(ceil(mouse.timedFF(1:1000:end))) % plots in seconds
        xlabel("time (s)")
        ylabel("normalized value")
        legend(["solenoid (CS)", "rewards", "forward velocity", "lickvoltage"])
    end
    mice{fl}=mouse;
    clear tr %remove condition from previous loop run
end

% average velocity of mouse e200
% days 2-5 = 3.6071
% days 8-14 = 12.4254
forwardvel=zeros(1,40000*4);
for i=2:5
    if i==2
        forwardvel = mice{i}.forwardvel;
    else
        forwardvel = [forwardvel mice{i}.forwardvel];
    end    
end
avvel_1 = mean(forwardvel);
% e201, days 8-14 = 13.0500
forwardvel=zeros(1,40000*5);
for i=15:19
    if i==15
        forwardvel = mice{i}.forwardvel;
    else
        forwardvel = [forwardvel mice{i}.forwardvel];
    end    
end
avvel_2 = mean(forwardvel);


% plot mean image per day
% e200: i=1:14; e201: 15:27
figure;
for i=42:54
    subplot(3,5,i-41)
    imagesc(mice{i}.ops.meanImg) %meanImg or max_proj
    colormap('gray')
    title(sprintf("day %i", i-41))
    axis off;
    hold on;    
    disp(i-41)
    disp(mice{i}.ops.save_path0)
end