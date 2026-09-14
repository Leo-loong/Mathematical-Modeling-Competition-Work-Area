function [iden,data,data1,n,m,n1,t,coo,kmat,pairid,nearid] = read(name,date,location,type)
% name = 'DoSA';date = '160914';location = 'F:\ÄªÀ¼µÙ\data';type = 1;
% name = 'SnWE';date = '200610';location = 'F:\ÄªÀ¼µÙ\data';type = 2;
    cd(location)
    switch type
        case 1
            spename = 'Radial';
            len = 4;
        case 2
            spename = 'Wave';
            len = 5;
        case 3
            spename = 'Wind';
            len = 10;
    end
    filenames = [];
    for i = 0:9
        for k = 0:5
            filenames = [filenames;[name,'_',date,'_','0',num2str(i),num2str(k),'0','_',spename,'.bin']];
        end
    end
    for i = 10:23
        for k = 0:5
            filenames = [filenames;[name,'_',date,'_',num2str(i),num2str(k),'0','_',spename,'.bin']];
        end
    end
    t = length(filenames);
    data = [];
    n = zeros(t,1);
    fileflag = 0;
    for filei = 1:t
        fileID = fopen(filenames(filei,:),'r','n','US-ASCII');
        if(fileID~=-1)
        head.name = fread(fileID,16,'*char')';
        head.data(1:5) = fread(fileID,5,'float');
        head.data(6) = fread(fileID,1,'double');
        head.data(7) = fread(fileID,1,'float');
        head.data(8:9) = fread(fileID,2,'int32');
        head.data(10:11) = fread(fileID,2,'float');
        head.data(12:13) = fread(fileID,2,'int32');
        head.des1 = fread(fileID,24,'*char')';
        head.des2 = fread(fileID,24,'*char')';
        head.des3 = fread(fileID,64,'*char')';
        head.des4 = fread(fileID,64,'*char')';
        head.des5 = fread(fileID,1,'int32');

        n(filei) = head.data(12);
        data(1:n(filei),filei,:) = nan(n(filei),1,4);
        data2 = zeros(n(filei),2);
        data3 = zeros(n(filei),len);% wave = 5,radial = 4
        for i = 1:n(filei)
            data(i,filei,:) = fread(fileID,4,'float');
            data2(i,:) = fread(fileID,2,'int32');
            data3(i,:) = fread(fileID,len,'float');
        end
        fclose(fileID);
        else
            fileflag = fileflag+1;
            disp(filenames(filei,:))
            disp(filei)
        end
    end
    data(:,:,1:3) = data(:,:,1:3)/pi*180;
    disp(['Number of files blocked:',' ',name,date,':',num2str(fileflag)])
    
    key = unique(data(:,:,1)+data(:,:,2)*1i);
    key(1) = [];
    coo = [imag(key),real(key)];
    n1 = length(key);
    data1 = nan(n1,t,4);
    flag = 0;
    for i = 1:t
        for j = 1:n(i)
            pos = find((data(j,i,1)+data(j,i,2)*1i)==key);
            if pos
                data1(pos,i,:) = data(j,i,:);
            else
                flag = flag+1;
            end
        end
    end
    m = sum(~isnan(data1(:,:,4)),2);
    ori = head.data(1:2);
    
    adjmat = nan(n1,n1);
    for i = 1:n1
        for j = 1:n1
            adjmat(i,j) = (real(key(i))-real(key(j)))^2+(imag(key(i))-imag(key(j)))^2;
        end
    end

    kmat = nan(n1,1);
    for i = 1:n1
            kmat(i) = (coo(i,2)-ori(2))/(coo(i,1)-ori(1));
    end

    pairid = nan(n1,2);
    nearid = nan(n1,100);
    range = head.data(11)/100;
    for id = 1:n1
        k = (coo(id,2)-ori(2))/(coo(id,1)-ori(1));
        for i = 1:2
            pair = [coo(id,1)+(-1)^i*range/(sqrt(1+k^2)),coo(id,2)+(-1)^i*range*k/(sqrt(1+k^2))];
            coodiff = sqrt(sum((coo-pair).^2,2));
            if min(coodiff)<range*0.3
                pairid(id,i) = find(coodiff==min(coodiff));
            else
                pairid(id,i) = id;
            end
        end
        [~,neartemp] = sort(adjmat(id,:));
        nearid(id,:) = neartemp(2:101);
    end
    
    rdist  = nan(n1,1);
    coor = coo*pi/180;
    orir = ori*pi/180;
    for i = 1:n1
        temp = sqrt(2*(1-cos(coor(i,2))*cos(orir(2))*cos(coor(i,1)-orir(1))-sin(coor(i,2))*sin(orir(2))));
        rdist(i) = asin(temp/2)*6000*2;
    end
    rdist = round(rdist*10)/10;
    radials = unique(rdist);
    rid = nan(n1,2);
    for i = 1:length(radials)
        rid(rdist==radials(i),2) = i;
        temp = find(rid(:,2)==i);
        temp1 = temp(coo(temp,1)>=ori(1));
        temp2 = temp(coo(temp,1)<ori(1));
        [~,s1] = sort(kmat(temp1),'descend');
        [~,s2] = sort(kmat(temp2),'descend');
        rid([temp1(s1);temp2(s2)],1) = 1:(length(s1)+length(s2));
    end
%     
%     plotid = 1:n1;
%     figure
%     scatter(coo(plotid,1),coo(plotid,2),[],rid(plotid,1))
%     axis equal
%     colorbar
%     
    iden = [name,date];
end