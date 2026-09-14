%mm1 simulation in matlab
%有优先级的MMm排队系统
%强插型
clc;clear;

ST_Idle=0;
ST_Busy=1;

EV_NULL=0;
EV_Arrive=1;
EV_Depart=2;
EV_LEN=3;

Q_LIMIT=1000;

% next_event_type=[];
% next_depart=[]            %因为有m个窗口，所以要确定下一个离开的是哪一个窗口的顾客
% num_custs_delayed=[];     %已到达的顾客数目
% num_delays_required=[];
% num_events=[];
% num_in_q=[];
% server_status=[];
% area_num_in_q=[];
% area_server_status=[];
% mean_interarrival=[];
% mean_service=[];
% sim_time=[];
% time_last_event=[];
% total_of_delays=[];
%
time_arrival=[];                 %顾客到达时刻,只是记录各级等待队列中顾客的到达时刻 ,该数组可能为空
time_arrival_II=[];
time_arrival_III=[];

time_next_event=zeros(1,EV_LEN);
%仿真参数
num_events=EV_LEN-1;
num_server=2;                     %M/M/m  m=2
% mean_interarrival=[30 300 100 50];%总的平均到达间隔和各类平均到达间隔
mean_interarrival=[30 150 100 60];%总的平均到达间隔和各类平均到达间隔

mean_service=20;
num_delays_required=20000;        %仿真要求到达的顾客数目

outfile=fopen('doctor.txt','w');
fprintf(outfile, 'Multiple-doctor queueing system\n\n');
fprintf(outfile, 'Mean interarrival time of all patients%26.3f minutes\n\n',mean_interarrival(1));
fprintf(outfile, 'Mean interarrival time of I patients%26.3f minutes\n\n',mean_interarrival(2));
fprintf(outfile, 'Mean interarrival time of II patients%26.3f minutes\n\n',mean_interarrival(3));
fprintf(outfile, 'Mean interarrival time of III patients%26.3f minutes\n\n',mean_interarrival(4));

fprintf(outfile, 'Mean service time%26.3f minutes\n\n', mean_service);
fprintf(outfile, 'Number of servers%26d\n\n', num_server);
fprintf(outfile, 'Number of customers%26d\n\n\n\n\n', num_delays_required);

%%%%%%%%%%%%%%%%%%%%%%%%% part1 initialize

sim_time=0.0;
    %/* Initialize the state variables. */

    server_status   =zeros(2,num_server);   %窗口状态
    server_status(2,:)=20;                  %正在服务的顾客级别,初始化为最低
    num_in_q        = zeros(1,4);           %解释类似于 total_of_delays
    time_last_event = 0.0;

    %/* Initialize the statistical counters. */

    num_custs_delayed  = zeros(1,4);        %解释类似于 total_of_delays
    total_of_delays    = zeros(1,4);        %第一个是所有级别客人的总等待时间，后三个各个级别客人的总的等待时间
    total_of_time    = 0.0;

    area_num_in_q      = zeros(1,4);
    area_server_status = 0.0;

    %/* Initialize event list.  Since no customers are present, the departure
    %(service completion) event is eliminated from consideration. */

    time_next_arrival=randexp(mean_interarrival);
    [time_next_arrival(1),rank_next_arrival]=min(time_next_arrival(2:4));
    server_status(2,1)=rank_next_arrival;       %第一个窗口顾客级别即为第一个将要到达的顾客等级
 time_next_event(EV_Arrive) = sim_time + time_next_arrival(1);

    time_next_event(EV_Depart) = 1.0e+230;

    time_depart=zeros(1,num_server);
    next_depart=0;                              %有顾客将要离开的窗口

%%%%%%%%%%%%%part2  Run the simulation while more delays are still needed.

while (num_custs_delayed(1) < num_delays_required)

    %/* Determine the next event. */

     min_time_next_event = 1.0e+290;
     next_event_type = 0;
    % Determine m depart event
     min_time_depart=1e290;
     next_depart=-1;
     for i=1:num_server
         if(server_status(i)==1 & time_depart(i)<min_time_depart)
             min_time_depart=time_depart(i);
             next_depart=i;
         end
     end
     time_next_event(EV_Depart)=min_time_depart;
%

    %/* Determine the event type of the next event to occur. */

    for i = 1: num_events
        if (time_next_event(i) < min_time_next_event)
            min_time_next_event = time_next_event(i);
            next_event_type     = i;
        end
    end

    %/* Check to see whether the event list is empty. */
    if (next_event_type == 0)
        fprintf(outfile, '\nEvent list empty at time %f', sim_time);
        exit(1);
    end
    %/* The event list is not empty, so advance the simulation clock. */

    sim_time = min_time_next_event;

    %/* Update time-average statistical accumulators. */

    double time_since_last_event;

    %/* Compute time since last event, and update last-event-time marker. */

    time_since_last_event = sim_time - time_last_event;
    time_last_event       = sim_time;

    %/* Update area under number-in-queue function. */要考虑优先级

    area_num_in_q(1)=area_num_in_q(1) +  num_in_q(1) * time_since_last_event;
    area_num_in_q(2)=area_num_in_q(2) +  num_in_q(2) * time_since_last_event;
    area_num_in_q(3)=area_num_in_q(3) +  num_in_q(3) * time_since_last_event;
    area_num_in_q(4)=area_num_in_q(4) +  num_in_q(4) * time_since_last_event;

    %/* Update area under server-busy indicator function. */

     for i=1:num_server
        area_server_status =area_server_status + server_status(1,i) * time_since_last_event;
    end

%arrival

    if(next_event_type==EV_Arrive)

%     %/* Schedule next arrival. */
%      time_next_arrival=randexp(mean_interarrival);
%      [time_next_arrival(1),rank_next_arrival]=min(time_next_arrival(2:4));
%      rank_next_arrival=rank_next_arrival-1;
%   time_next_event(EV_Arrive) = sim_time + time_next_arrival(1);
%       time_next_event(1) = sim_time + randexp(mean_interarrival);

    %/* Check to see whether server is busy. */

        s_idle=-1;
        for i=1:num_server
            if (server_status(1,i) == ST_Idle)
                s_idle=i;
                break;
            end
        end

        %所有窗口忙，考虑优先级，强插情形
        if(s_idle== -1 )
                if(rank_next_arrival < max(server_status(2,:)))                 %可以挤掉正在服务的最低级顾客
                    [temp_rank,temp_server]=max(server_status(2,:));
                    num_in_q(1)=1+num_in_q(1);                                  %所有排队队列中人数加一
                    num_in_q(1+temp_rank)=1+num_in_q(1+temp_rank);

                    if (num_in_q(1) > Q_LIMIT)                                  %检查等待队列是否满
                     %/* 等待队列溢出，停止仿真*/
                     fprintf(outfile, '\nOverflow of the array time_arrival at');
                    fprintf(outfile, ' time %f', sim_time);
                    exit(2);
                    else

                    if temp_rank==1                                             %被挤掉顾客放在相应等待队列首位，记录时间
                        time_arrival=[sim_time,time_arrival];
                    elseif temp_rank==2;
                        time_arrival_II=[sim_time,time_arrival_II];
                    else
                        time_arrival_III=[sim_time,time_arrival_III];
                    end
                    server_status(2,temp_server)=rank_next_arrival;

                end

            %不能挤掉已有顾客
            else
                num_in_q(1)=1+num_in_q(1);
                num_in_q(1+rank_next_arrival)=1+num_in_q(1+rank_next_arrival);  %相应等级的等待队列中加一

                %/* Check to see whether an overflow condition exists. */

                if (num_in_q(1) > Q_LIMIT)
                %/* 等待队列溢出，停止仿真*/

                    fprintf(outfile, '\nOverflow of the array time_arrival at');
                    fprintf(outfile, ' time %f', sim_time);
                    exit(2);
                else
                    %/* There is still room in the queue, so store the time of arrival of the arriving customer at the (new) end of time_arrival. */
                    %队列中还有空间，刚达到顾客入队，到达时间插入队列尾部
                    %设三个等待队列
                    if rank_next_arrival==1
                        time_arrival=[time_arrival,sim_time];
                    elseif rank_next_arrival==2
                        time_arrival_II=[time_arrival_II,sim_time];
                    else
                        time_arrival_III=[time_arrival_III,sim_time];
                    end
                end
            end

        %有空闲窗口，来的顾客等待时间为零
        else
            delay = 0.0;
            total_of_delays(1) =total_of_delays(1) + delay;
            total_of_delays(1+rank_next_arrival) =total_of_delays(1+rank_next_arrival) + delay;

        %已经到达顾客数目加一，标记窗口状态，顾客级别

            num_custs_delayed(1) = 1 + num_custs_delayed(1);
            num_custs_delayed(1+rank_next_arrival)=num_custs_delayed(1+rank_next_arrival)+1;
            server_status(1,s_idle) = ST_Busy;
            server_status(2,s_idle) = rank_next_arrival;

        %/*安排正在服务的顾客的服务时间长度，即离开时间*/

            time_depart(s_idle) = sim_time + randexp(mean_service);
        end

%???????
        %/* Schedule next arrival. */决定下一个将要到达的顾客的到达时刻

%      time_next_arrival=randexp(mean_interarrival);

        time_next_arrival(1+rank_next_arrival) =  randexp(mean_interarrival(1+rank_next_arrival));

        [time_next_arrival(1),rank_next_arrival]=min(time_next_arrival(2:4));
  time_next_event(EV_Arrive) = sim_time + time_next_arrival(1);

%depart

    else
         double delay;

        %/* Check to see whether the queue is empty. */

        if (num_in_q(1) == 0)

        % /* The queue is empty so make the server idle and eliminate the departure (service completion) event from consideration. */

            server_status(1,next_depart)      = ST_Idle;
            time_depart(next_depart) = 1.0e+230;
            %check_depart()
            min_time_depart=1e290;
            next_depart=-1;
            for i=1:num_server
                if(server_status(1,i)==1 & time_depart(i)<min_time_depart)
                    min_time_depart=time_depart(i);
                    next_depart=i;
                end
            end
            time_next_event(EV_Depart)=min_time_depart;

        else
        %等待队列非空，等待队列中顾客补上时，要考虑优先级
            num_in_q(1)=num_in_q(1)-1;
            for i=server_status(2,next_depart):3
                if(num_in_q(1+i)>=1)
                    num_in_q(1+i)=num_in_q(1+i)-1;
                    break;
                end
            end
            server_status(2,next_depart)=i;

        %/* Compute the delay of the customer who is beginning service and update the total delay accumulator. */
        %刚补上的顾客的等待时间，因为有优先级，补上的不一定是等待时间最长的那一个
            if i==1
                delay = sim_time - time_arrival(1);
                tempForPop=time_arrival(2:length(time_arrival));
                time_arrival=tempForPop;
            elseif i==2
                delay = sim_time - time_arrival_II(1);
                tempForPop=time_arrival_II(2:length(time_arrival_II));
                time_arrival_II=tempForPop;
            else
                delay = sim_time - time_arrival_III(1);
                tempForPop=time_arrival_III(2:length(time_arrival_III));
                time_arrival_III=tempForPop;
            end
            total_of_delays(1) =total_of_delays(1) + delay;
            total_of_delays(1+i)=total_of_delays(1+i) + delay;

        %/* Increment the number of customers delayed, and schedule departure. */

            num_custs_delayed(1) = 1 + num_custs_delayed(1);
            num_custs_delayed(1+i)=num_custs_delayed(1+i) + 1;
            serv_time=randexp(mean_service);
            time_depart(next_depart) = sim_time + serv_time;
            total_of_time = total_of_time + delay + serv_time;
            %check_depart()
            min_time_depart=1e290;
            next_depart=-1;
            for i=1:num_server
                if(server_status(i)==1 & time_depart(i)<min_time_depart)
                    min_time_depart=time_depart(i);
                    next_depart=i;
                end
            end
            time_next_event(2)=min_time_depart;

        %/* Move each customer in queue (if any) up one place. */
        %因为有三个等级，故设三个等待队列
%             tempForPop=time_arrival(2:length(time_arrival));
%             time_arrival=tempForPop;
%             tempForPop=time_arrival_II(2:length(time_arrival_II));
%             time_arrival_II=tempForPop;
%             tempForPop=time_arrival_III(2:length(time_arrival_III));
%             time_arrival_III=tempForPop;

        end %if (num_in_q == 0)

    end %if(next_event_type==EV_Arrive)

end %while

%%%%%%%%%% part3    Invoke the report generator and end the simulation. */

    fprintf(outfile, '\n\nAverage delay in all queue%26.3f minutes\n\n',total_of_delays(1) / num_custs_delayed(1));
    fprintf(outfile, '\n\nAverage delay in queue I  %26.3f minutes\n',total_of_delays(2)/num_custs_delayed(2));
    fprintf(outfile, '\n\nAverage delay in queue II  %26.3f minutes\n',total_of_delays(3) / num_custs_delayed(3));
    fprintf(outfile, '\n\nAverage delay in queue III  %26.3f minutes\n\n',total_of_delays(4) / num_custs_delayed(4));

    fprintf(outfile, '\n\nAverage delay in system%26.3f minutes\n\n',total_of_time / num_custs_delayed(1));

    fprintf(outfile, 'Average number in queue%26.3f\n\n',area_num_in_q(1) / sim_time);
    fprintf(outfile, 'Server utilization%26.3f\n\n',area_server_status / sim_time);
    fprintf(outfile, 'Time simulation ended%26.3f minutes', sim_time);
    fclose(outfile);
