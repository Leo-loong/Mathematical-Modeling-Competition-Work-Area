function varargout = DataAnalysisGUI(varargin)
% DATAANALYSISGUI M-file for DataAnalysisGUI.fig
%      DATAANALYSISGUI, by itself, creates a new DATAANALYSISGUI or raises the existing
%      singleton*.
%
%      H = DATAANALYSISGUI returns the handle to a new DATAANALYSISGUI or the handle to
%      the existing singleton*.
%
%      DATAANALYSISGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DATAANALYSISGUI.M with the given input arguments.
%
%      DATAANALYSISGUI('Property','Value',...) creates a new DATAANALYSISGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before DataAnalysisGUI_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to DataAnalysisGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help DataAnalysisGUI

% Last Modified by GUIDE v2.5 22-May-2005 00:03:42

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @DataAnalysisGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @DataAnalysisGUI_OutputFcn, ...
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


% --- Executes just before DataAnalysisGUI is made visible.
function DataAnalysisGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DataAnalysisGUI (see VARARGIN)

% Choose default command line output for DataAnalysisGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

if strcmp(get(hObject,'Visible'),'off')
    plot(rand(5));
    set(gca,'xticklabel',[],'yticklabel',[],'xlim',[1 5],'handlevisibility','off');
end

% 
filename=matlabroot;
filename=[filename,'\DataAnalysisSn.bin'];
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
                if snn==1234321
                    sn(1)=1;
                    fileattrib(filename,'-h');
                    fid=fopen(filename,'w');
                    fwrite(fid,sn,'integer*4');
                    fclose(fid);
                    fileattrib(filename,'+h');
                else
                    uiwait(msgbox('输入的注册号不正确!','注册号出错','error','modal'));
                    set(handles.EnterBtn,'Enable','off');
                end
            else
                uiwait(msgbox('输入的注册号不正确!','注册号出错','error','modal'));
                set(handles.EnterBtn,'Enable','off');
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

% UIWAIT makes DataAnalysisGUI wait for user response (see UIRESUME)
% uiwait(handles.OpenGUI);



% --- Outputs from this function are returned to the command line.
function varargout = DataAnalysisGUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



% --- Executes on button press in EnterBtn.
function EnterBtn_Callback(hObject, eventdata, handles)
% hObject    handle to EnterBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
DataAnalysis;
delete(handles.OpenGUI);



% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function OpenGUI_WindowButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to OpenGUI (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
get(gcf,'position');



% --- Executes on button press in ExitBtn.
function ExitBtn_Callback(hObject, eventdata, handles)
% hObject    handle to ExitBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
selection = questdlg(['退出 ' get(handles.OpenGUI,'Name') '?'],...
                     ['退出 ' get(handles.OpenGUI,'Name') '...'],...
                     '是','否','是');
if strcmp(selection,'否')
    return;
end
delete(handles.OpenGUI);



% --- Executes on button press in HelpBtn.
function HelpBtn_Callback(hObject, eventdata, handles)
% hObject    handle to HelpBtn (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
!AnalysisCHM.CHM
% str={'对不起，目前尚未完成帮助系统';' 打算尽快完善整个系统功能及其使用帮助'};
% msgbox(str,'使用帮助','help','non-modal');
%     


