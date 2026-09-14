function varargout = DataAnalysis(varargin)

% Edit the above text to modify the response to help DataAnalysis

% Last Modified by GUIDE v2.5 23-May-2005 18:23:48

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @DataAnalysis_OpeningFcn, ...
                   'gui_OutputFcn',  @DataAnalysis_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin & isstr(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT




% --- Executes just before DataAnalysis is made visible.
function DataAnalysis_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DataAnalysis (see VARARGIN)

% Choose default command line output for DataAnalysis
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

axes(handles.axes1);
plot(rand(20,8));
set(gca,'xticklabel',[],'xtick',[]);
axes(handles.axes2);
plot(rand(20,8));
set(gca,'xticklabel',[],'xtick',[]);
set(gcf,'DoubleBuffer','on');

% UIWAIT makes DataAnalysis wait for user response (see UIRESUME)
% uiwait(handles.figmain);
filename=matlabroot;
filename=[filename,'\DataAnalysisSn2.bin'];
if(exist(filename)==0)
    fid=fopen(filename,'w+');
    fileattrib(filename,'+h');
    sn=[0,1];
    fwrite(fid,sn,'integer*4');
    fclose(fid);
else
    fid=fopen(filename,'r');
    sn=fread(fid,2,'int32');
    fclose(fid);
    if(sn(1)==0)
        num=sn(2)+1;
        sn(2)=num;
        if(num>500)
            answer=inputdlg('请输入注册号:','注册');
            if(~isempty(answer))
                str=answer{1};
                snn=str2num(str);
                if snn==9876789
                    sn(1)=1;
                    fileattrib(filename,'-h');
                    fid=fopen(filename,'w');
                    fwrite(fid,sn,'integer*4');
                    fclose(fid);
                    fileattrib(filename,'+h');
                else
                    uiwait(msgbox('输入的注册号不正确!','注册号出错','error','modal'));
                    set(handles.preProcess,'Enable','off');
                end
            else
                uiwait(msgbox('输入的注册号不正确!','注册号出错','error','modal'));
                set(handles.preProcess,'Enable','off');
            end
        else
            fileattrib(filename,'-h');
            fid=fopen(filename,'w');
            fwrite(fid,sn,'integer*4');
            fclose(fid);
            fileattrib(filename,'+h');
        end
    end
end


% --- Outputs from this function are returned to the command line.
function varargout = DataAnalysis_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function figmain_WindowButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to figmain (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
get(gcf,'position');



% --- Executes on button press in Open.
function Open_Callback(hObject, eventdata, handles)
% hObject    handle to Open (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.classRun,'Enable','off');
[filename, pathname] = uigetfile('*.xls', '打开excel文件');
if isequal(filename,0) | isequal(pathname,0)
    set(handles.fileopen,'string','尚未打开文件');
    set(handles.sheetopen,'string','尚未选择表单');
    set(handles.xianshi,'visible','on');
    set(handles.resultShuomin,'string','');
    set(handles.sheetlist,'string',{'表单名',''});
    axes(handles.axes1);
    plot(rand(20,8));
    axes(handles.axes2);
    plot(rand(20,8));
    set(handles.shuomin,'visible','on');
    return;
else
    strindex=strfind(filename,'.');
    str=filename(1:strindex-1);
    set(handles.fileopen,'string',str);
    pathfile=[pathname,filename];
    watchon;
    [A, sheetnames] = XLSFINFO(pathfile);
    set(handles.sheetlist,'string',sheetnames');
    set(handles.sheetopen,'string',sheetnames{1});
    watchoff;
    set(handles.Open,'UserData',pathfile);
    set(handles.sheetlist,'UserData',sheetnames{1});
    set(handles.classRun,'Enable','off');
end


% --- Executes during object creation, after setting all properties.
function sheetlist_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sheetlist (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end




% --- Executes on selection change in sheetlist.
function sheetlist_Callback(hObject, eventdata, handles)
% hObject    handle to sheetlist (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns sheetlist contents as cell array
%        contents{get(hObject,'Value')} returns selected item from sheetlist
itemvalue=get(hObject,'Value');
contents = get(hObject,'String');
sheetname=contents{itemvalue};
set(handles.sheetopen,'string',sheetname);
set(hObject,'UserData',sheetname);



% --------------------------------------------------------------------
function Exit_Callback(hObject, eventdata, handles)
% hObject    handle to Exit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

selection = questdlg('退出数据相关性分析系统?','退出系统...', '是','否','是');
if strcmp(selection,'否')
    return;
end
delete(handles.figmain);



% --- Executes on button press in labelpoint.
function labelpoint_Callback(hObject, eventdata, handles)
% hObject    handle to labelpoint (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
outers=getappdata(handles.figmain,'outers');
m=size(outers,1);
axes(handles.axes1);
legendCkb_Callback(hObject, eventdata, handles);
hold on
for k=1:m
    X=outers{k,1};
    Y=outers{k,2};
    plot(X,Y,'r+');
end

hold off
   



% --- Executes during object creation, after setting all properties.
function processMethod_CreateFcn(hObject, eventdata, handles)
% hObject    handle to processMethod (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end



% --- Executes on selection change in processMethod.
function processMethod_Callback(hObject, eventdata, handles)
% hObject    handle to processMethod (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns processMethod contents as cell array
%        contents{get(hObject,'Value')} returns selected item from processMethod
processMethod=get(hObject,'Value');
switch processMethod
    case 1, % 均方误差方法
        str={'','  计算出各标列与标准列之间的','  偏差的平方和的均值','其值越小说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    case 2, % 拟合优度法
        str={'','看成用非标准列数据去拟合标准数据','根据拟合的优度评价标准进行评价','其值越接近于1说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    case 3, %相关系数法
        str={'','根据非标准列数据与标准数据的相关性','根据相关系数评价标准进行评价','其值越接近于1说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    case 4, %频谱分析法
        str={'','分析标准数据与非标准数据的频谱特性','根据与标准谱线的幅值均方差进行评价','其值越小说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    case 5, % 归一化内积法
        str={'','分析标准数据与非标准数据的归一化内积','根据归一化内积来进行相似程度的评价','其值越大说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    case 6, % Camberra距离度量
        str={'','分析与标准数据的Camberra距离','根据Camberra距离的均值进行评价','其值越小说明该列与标准值越接近'};
        set(handles.methodShuomin,'String',str);
    otherwise,
        msgbox('不会吧，这也能够出现?');
end
set(hObject,'UserData',processMethod);




% --- Executes during object creation, after setting all properties.
function preProcessMethode_CreateFcn(hObject, eventdata, handles)
% hObject    handle to preProcessMethode (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc
    set(hObject,'BackgroundColor','white');
else
    set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'));
end




% --- Executes on selection change in preProcessMethode.
function preProcessMethode_Callback(hObject, eventdata, handles)
% hObject    handle to preProcessMethode (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = get(hObject,'String') returns preProcessMethode contents as cell array
%        contents{get(hObject,'Value')} returns selected item from preProcessMethode
methodVal=get(hObject,'Value');
set(hObject,'UserData',methodVal);




% --- Executes on button press in preProcess.
function preProcess_Callback(hObject, eventdata, handles)
% hObject    handle to preProcess (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
filename=get(handles.Open,'UserData');
sheetname=get(handles.sheetlist,'UserData');
try
    [data,colName]=xlsread(filename,sheetname);
catch
    if(isempty(sheetname)||isempty(filename))
        uiwait(msgbox('没有打开数据文件!','读取文件出错','error','modal'));
        return;
    end
    uiwait(msgbox('xls文件保存格式不对!','读取文件出错','error','modal'));
    return;
end    
originData=data(3:end,2:end);
setappdata(handles.figmain,'originData',originData);
fieldNames(1,:)=colName(2,2:end);
% setappdata(handles.figmain,'fieldName',fieldNames);
set(handles.shuomin,'visible','off');
axes(handles.axes1);
plot(originData);
legendCkbVal=get(handles.legendCkb,'value');
watchon;
legendLabel=fieldNames;
n1=size(originData,2);
n2=size(fieldNames,2);
for k=(n2+1):n1
    str=sprintf('No. %d',k);
    legendLabel={legendLabel{:},str};
end
setappdata(handles.figmain,'fieldName',legendLabel);
if legendCkbVal
    legend(legendLabel);
end
method=get(handles.preProcessMethode,'UserData');
switch method % 输入原始数据（非标准数据）；输出各列的粗大误差的下标与坐标
    case 1, % 3S 原则 
        outers = laYiDa(originData(:,2:end));  % outers的格式为: 下标(x坐标),y值
    case 2, % 分布图法
        outers = fenBuTu(originData(:,2:end));
    otherwise,
        msgbox('不可能出现的吧?');
end
setappdata(handles.figmain,'outers',outers);
watchoff;      
set(handles.classRun,'Enable','on');




% --------------------------------------------------------------------
function help_Callback(hObject, eventdata, handles)
% hObject    handle to help (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --------------------------------------------------------------------
function helpRun_Callback(hObject, eventdata, handles)
% hObject    handle to helpRun (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
!AnalysisCHM.CHM
% str={'对不起，目前尚未完成帮助系统';' 打算尽快完善整个系统功能及其使用帮助'};
% msgbox(str,'使用帮助','help','non-modal');





% --------------------------------------------------------------------
function about_Callback(hObject, eventdata, handles)
% hObject    handle to about (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
str={'';'             数据分析系统';'             设计者: 莫燃';'              2004.5 '};
Data=1:64;Data=(Data'*Data)/64;
msgbox(str,'关于...','custom',Data,hot(64));




% --- Executes on button press in legendCkb.
function legendCkb_Callback(hObject, eventdata, handles)
% hObject    handle to legendCkb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of legendCkb
legendCkbVal=get(handles.legendCkb,'value');
if legendCkbVal
    legendLabel=getappdata(handles.figmain,'fieldName');
    n1=size(getappdata(handles.figmain,'originData'),2);
    n2=size(legendLabel,2);
    for k=(n2+1):n1
        str=sprintf('No. %d',k);
        legendLabel={legendLabel{:},str};
    end
    if(~isempty(legendLabel))
        legend(legendLabel);
    end
else
    legend off;
end




% --- Executes on button press in helpBtn.
function helpBtn_Callback(hObject, eventdata, handles)
% hObject    handle to helpBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --- Executes on button press in exitBtn.
function exitBtn_Callback(hObject, eventdata, handles)
% hObject    handle to exitBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)




% --- Executes on button press in classRun.
function classRun_Callback(hObject, eventdata, handles)
% hObject    handle to classRun (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
watchon;
set(handles.xianshi,'Visible','off');
processMethod=get(handles.processMethod,'UserData');
originData=getappdata(handles.figmain,'originData');
fieldName=getappdata(handles.figmain,'fieldName');
outers=getappdata(handles.figmain,'outers');
switch processMethod
    case 1, % 均方误差方法
        resultData=fangchahe(originData,outers); % resultData为一个包含结果的向量
        [bestData,bestIndex]=min(resultData(2:end));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
        
    case 2, % 拟合优度法
        resultData=liheyoudu(originData,outers);
        [bestData,bestIndex]=max(resultData(2:end));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
        
    case 3, %相关系数法
        resultData=corrcoeffa(originData,outers);
        [bestData,bestIndex]=min(abs(resultData(2:end)-1));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
    case 4, %频谱分析法
        resultData=fftfa(originData,outers);
        [bestData,bestIndex]=min(resultData(2:end));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
        
    case 5, % 归一化内积法
        resultData=leijifa(originData,outers);
        [bestData,bestIndex]=max(resultData(2:end));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
        
    case 6, % Camberra距离度量
        resultData=camberra(originData,outers);
        [bestData,bestIndex]=min(resultData(2:end));
        bestIndex=bestIndex+1;
        axes(handles.axes2);
        bar(resultData);
        
%     case 7, % Mahalanobis距离
%         resultData=mahalanobis(originData,outers);
%         [bestData,bestIndex]=min(resultData(2:end));
%         bestIndex=bestIndex+1;
%         axes(handles.axes2);
%         bar(resultData);
        
    otherwise,
        msgbox('不会吧，这也能够出现?');
end


n1=size(originData,2);
n2=size(fieldName,2);
for k=(n2+1):n1
    str=sprintf('No. %d',k);
    fieldName={fieldName{:},str};
end
set(handles.resultShuomin,'String',{'',fieldName{bestIndex}});
setappdata(handles.figmain,'ResultData',resultData);
watchoff;




% --- Executes on button press in resultSave.
function resultSave_Callback(hObject, eventdata, handles)
% hObject    handle to resultSave (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[filename, pathname] = uiputfile('*.txt', '保存分析结果');
pathfile=[pathname,filename,'.txt'];
watchon;
try
fid=fopen(pathfile,'wt');
fprintf(fid,'\n\n');
fprintf(fid,'数据相关性分析结果记录\n\n');
d2=NOW;
timestr=datestr(d2,31);
fprintf(fid,'实验时间: \t%s',timestr);
fprintf(fid,'\n\n');
fprintf(fid,'------------------------------------------------------------------\n');
fprintf(fid,['数据文件名称:\t',get(handles.fileopen,'string')]);
fprintf(fid,'\n');
fprintf(fid,['数据表单名称:\t',get(handles.sheetopen,'string')]);
fprintf(fid,'\n');
contents=get(handles.preProcessMethode,'string');
str=contents{get(handles.preProcessMethode,'Value')};
fprintf(fid,['剔除粗大误差方法:\t',str]);
fprintf(fid,'\n');
contents=get(handles.processMethod,'string');
str=contents{get(handles.processMethod,'Value')};
fprintf(fid,['相似程度分析方法:\t',str]);
fprintf(fid,'\n相似程度分析方法说明:\n');
shuominstr=get(handles.methodShuomin,'string');
num=size(shuominstr,1);
for k=1:num
    fprintf(fid,'\t\t');
    fprintf(fid,shuominstr{k});
    fprintf(fid,'\n');
end

% getappdata(handles.figmain,'originData');
% getappdata(handles.figmain,'fieldName');
% outers=getappdata(handles.figmain,'outers');
% setappdata(handles.figmain,'ResultData',resultData);
outers=getappdata(handles.figmain,'outers');
fieldnames=getappdata(handles.figmain,'fieldName');
result=getappdata(handles.figmain,'ResultData');
n=size(outers,1);
fprintf(fid,'\n-----------------------------------------------------------------\n');
for k=2:n+1
    fprintf(fid,[fieldnames{k},'\n']);
    fprintf(fid,'\t剔除的粗大误差点为:\t');
    outerstr=mat2str(outers{k-1,2});
    fprintf(fid,outerstr);
    fprintf(fid,'\n');
    fprintf(fid,'\t相似程度结果为:\t\t');
    resultstr=num2str(result(k));
    fprintf(fid,resultstr);
    fprintf(fid,'\n\n');
end
fprintf(fid,'\n-----------------------------------------------------------------\n\n');
fprintf(fid,'其中与标准样本最接近的是：\t');
str=get(handles.resultShuomin,'string');
fprintf(fid,str{2});
fprintf(fid,'\n\n');
fclose(fid);

catch
end
watchoff;




% --------------------------------------------------------------------
function zoomIn_Callback(hObject, eventdata, handles)
% hObject    handle to zoomIn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% axes(handles.axes1);
zoom(1.5);




% --------------------------------------------------------------------
function zoomOut_Callback(hObject, eventdata, handles)
% hObject    handle to zoomOut (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% axes(handles.axes1);
zoom(0.8);





% --------------------------------------------------------------------
function zoomBoth_Callback(hObject, eventdata, handles)
% hObject    handle to zoomBoth (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



% --------------------------------------------------------------------
function grant_Callback(hObject, eventdata, handles)
% hObject    handle to grant (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
zoom on



% --------------------------------------------------------------------
function forbid_Callback(hObject, eventdata, handles)
% hObject    handle to forbid (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
zoom off;







% ===============================================================================
% 以下为相似度判别函数
%-------------------------------------------------------------------------------
function resultData=camberra(originData,outers)
% camberra.m
% Camberra距离度量法
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5

[m,n]=size(originData);
resultData=zeros(1,n);
resultData(1)=0;
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    num=length(stdData);
    absSub=abs(tempData-stdData);
    absAdd=abs(tempData+stdData);
    tempResult=sum(absSub./absAdd);
    resultData(k)=tempResult/num;
end




%-------------------------------------------------------------------------------
function resultData=fangchahe(originData,outers)
% fangchahe.m
% 误差平方和方法评判
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5

[m,n]=size(originData);
resultData=zeros(1,n);
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    tempSub=abs(stdData-tempData);
    tempResult=tempSub.^2;
    resultData(k)=mean(tempResult);
end




%-------------------------------------------------------------------------------
function resultData=liheyoudu(originData,outers)
% liheyoudu.m
% 拟合优度法评判
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5
%%%------------此方法还待思考

[m,n]=size(originData);
resultData=zeros(1,n);
resultData(1)=1;
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    sse=sum((stdData-tempData).^2);
    num=length(stdData);
    sst=sum(stdData.^2)-(sum(stdData))^2/num;
    resultData(k)=1-sse/sst;
end




%-------------------------------------------------------------------------------
function resultData=corrcoeffa(originData,outers)
% corrcoeffa.m
% 相关系数法评判
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5

[m,n]=size(originData);
resultData=zeros(1,n);
resultData(1)=1;
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    tempResult=corrcoef(stdData,tempData);
    resultData(k)=tempResult(2);
end




%-------------------------------------------------------------------------------
function resultData=fftfa(originData,outers)
% fftfa.m
% 幅频分析方法评判
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5

[m,n]=size(originData);
resultData=zeros(1,n);
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    stdDataFft=fft(stdData);
    tempDataFft=fft(tempData);
    tempFftAbs=abs(tempDataFft);
    stdFftAbs=abs(stdDataFft);
    num=length(tempFftAbs);
    tempSub=tempFftAbs-stdFftAbs;
    tempResult=sum(tempSub.^2);
    resultData(k)=tempResult/num;   
end





%-------------------------------------------------------------------------------
function  resultData=leijifa(originData,outers)
% leijifa.m
% 采用归一化内积判断两个向量的相似度
% 输入: 原始数据，粗大误差点
% 输出: 各列与标准数据的误差
% 2004.5

[m,n]=size(originData);
resultData=zeros(1,n);
resultData(1)=1;
for k=2:n
    stdData=originData(:,1);
    tempData=originData(:,k);
    outerIndex=outers{k-1,1};
    stdData(outerIndex)=[];
    tempData(outerIndex)=[];
    fenzi=stdData'*tempData;
    fenmu1=(sum(stdData.^2))^(0.5);
    fenmu2=(sum(tempData.^2))^(0.5);
    fenmu=fenmu1*fenmu2;
    resultData(k)=fenzi/fenmu;
end


% =============================================================================







% ==============================================================================
%  以下为剔除粗大误差函数

% ------------------------------------------------------------------------------
function outers = fenBuTu(originData)
%  采用拉分布图法剔除粗大误差点
%  输出参数为cell矩阵
%  2004.5

[m,n]=size(originData);
outers=cell(n,2);
for k=1:n % 对各列分别处理
    Data=originData(:,k);
    sortData=sort(Data);
    rownum=size(sortData,1);
    % 算中位数
    if mod(rownum,2) % 奇数个样本点
        Xm=sortData((rownum+1)/2);
        % 算四分位数
        lcol=sortData(1:round((rownum+1)/2));
        ucol=sortData(round((rownum+1)/2):end);
        rownum2=size(lcol,1);
        if mod(rownum2,2) 
            F1=lcol(round((rownum2+1)/2));
            F0=ucol(round((rownum2+1)/2));
        else
            F1=(lcol(round(rownum2/2+1))+lcol(round(rownum2/2)))/2;
            F0=(ucol(round(rownum2/2+1))+ucol(round(rownum2/2)))/2;
        end
    else
        Xm=(Data(round(rownum/2+1))+Data(round(rownum/2)))/2;
        % 算四分位数
        lcol=sortData(1:round((rownum+1)/2));
        ucol=sortData(round((rownum+1)/2):end);
        rownum2=size(lcol,1);
        if mod(rownum2,2) 
            F1=lcol(round((rownum2+1)/2));
            F0=ucol(round((rownum2+1)/2));
        else
            F1=(lcol(round(rownum2/2+1))+lcol(round(rownum2/2)))/2;
            F0=(ucol(round(rownum2/2+1))+ucol(round(rownum2/2)))/2;
        end
    end
        
    dF=F0-F1;     % 四分位数离散度
    beta=2;       % 精度常数
    ruo1=F1-beta/2*dF;
    ruo2=F0+beta/2*dF;
    outerindex=find(Data<ruo1|Data>ruo2);
    outercoor=Data(outerindex);
    outers{k,1}=outerindex;
    outers{k,2}=outercoor;
end
  



%-------------------------------------------------------------------------------
function  outers = laYiDa(originData)
% laYiDa,m
%  采用拉依达法剔除粗大误差点
%  输出参数为cell矩阵
%  2004.5

[m,n]=size(originData);
outers=cell(n,2);
for k=1:n
    colData=originData(:,k);
    outercoor=findouter(colData);  % 找出列的outer
    outerindex=[];
    outercoor2=[];
    for num=1:length(outercoor)
        tempcoor=outercoor(num);
        tempindex=find(abs(colData-tempcoor)<0.1);
        tempcoor=tempcoor*ones(length(tempindex),1); % 避免出现相同值的情况露选
        outerindex=[outerindex;tempindex];
        outercoor2 =[outercoor2;tempcoor];
    end
    outers{k,1}=outerindex;
    outers{k,2}=outercoor2;
end





%-------------------------------------------------------------------------------
function coor=findouter(colset)
%采用递归的方法剔除outer
colStd = std(colset);
colMean = mean(colset);
colSub = abs(colset-colMean);
index=find(colSub>(2.8*colStd));
coor=colset(index);
if(isempty(index))
    return;
else
    colset(index)=[];
    tempcoor=findouter(colset);
    coor=[coor;tempcoor];
end
