classdef picture_plot < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                matlab.ui.Figure
        Panel_2                 matlab.ui.container.Panel
        DropDown_3              matlab.ui.control.DropDown
        Label_11                matlab.ui.control.Label
        cm8cm128EditFieldLabel  matlab.ui.control.Label
        cm8cm128EditField       matlab.ui.control.EditField
        Button_8                matlab.ui.control.Button
        Button_7                matlab.ui.control.Button
        Button_2                matlab.ui.control.Button
        UITable_2               matlab.ui.control.Table
        UITable                 matlab.ui.control.Table
        Button                  matlab.ui.control.Button
        TabGroup                matlab.ui.container.TabGroup
        Tab                     matlab.ui.container.Tab
        EditField_17Label       matlab.ui.control.Label
        EditField_17            matlab.ui.control.EditField
        DropDown_11             matlab.ui.control.DropDown
        DropDown_11Label        matlab.ui.control.Label
        DropDown_10             matlab.ui.control.DropDown
        Label_20                matlab.ui.control.Label
        Label_19                matlab.ui.control.Label
        DropDown_9              matlab.ui.control.DropDown
        DropDown_9Label         matlab.ui.control.Label
        DropDown_8              matlab.ui.control.DropDown
        Panel                   matlab.ui.container.Panel
        Label_22                matlab.ui.control.Label
        EditField_16            matlab.ui.control.EditField
        Label_18                matlab.ui.control.Label
        EditField_15            matlab.ui.control.EditField
        Label_13                matlab.ui.control.Label
        EditField_13            matlab.ui.control.EditField
        Label_21                matlab.ui.control.Label
        EditField_11            matlab.ui.control.EditField
        EditField_10Label       matlab.ui.control.Label
        EditField_10            matlab.ui.control.EditField
        EditField_9Label        matlab.ui.control.Label
        EditField_9             matlab.ui.control.EditField
        Panel_4                 matlab.ui.container.Panel
        DropDown_7              matlab.ui.control.DropDown
        Label_16                matlab.ui.control.Label
        DropDown_5              matlab.ui.control.DropDown
        Label_14                matlab.ui.control.Label
        y23y23Label             matlab.ui.control.Label
        y23y23EditField         matlab.ui.control.EditField
        xx101lengthyEditField   matlab.ui.control.EditField
        x1lengthyLabel          matlab.ui.control.Label
        DropDown                matlab.ui.control.DropDown
        Button_9                matlab.ui.control.Button
        Panel_3                 matlab.ui.container.Panel
        Label_6                 matlab.ui.control.Label
        EditField_5             matlab.ui.control.EditField
        Label_5                 matlab.ui.control.Label
        EditField_4             matlab.ui.control.EditField
        DropDown_4              matlab.ui.control.DropDown
        DropDown_4Label         matlab.ui.control.Label
        TabGroup2               matlab.ui.container.TabGroup
        Tab_4                   matlab.ui.container.Tab
        Label_8                 matlab.ui.control.Label
        EditField_7             matlab.ui.control.EditField
        Label_7                 matlab.ui.control.Label
        EditField_6             matlab.ui.control.EditField
        Label_3                 matlab.ui.control.Label
        EditField_3             matlab.ui.control.EditField
        DropDown_2              matlab.ui.control.DropDown
        Label_4                 matlab.ui.control.Label
        Label_9                 matlab.ui.control.Label
        EditField_8             matlab.ui.control.EditField
        EditFieldLabel          matlab.ui.control.Label
        EditField               matlab.ui.control.EditField
        yEditFieldLabel         matlab.ui.control.Label
        yEditField              matlab.ui.control.EditField
        xEditFieldLabel         matlab.ui.control.Label
        xEditField              matlab.ui.control.EditField
        Tab_5                   matlab.ui.container.Tab
        yLabel_3                matlab.ui.control.Label
        yEditField_2            matlab.ui.control.EditField
        xLabel_3                matlab.ui.control.Label
        xA1A2EditField          matlab.ui.control.EditField
        yLabel_2                matlab.ui.control.Label
        y12100EditField         matlab.ui.control.EditField
        xLabel_2                matlab.ui.control.Label
        x134EditField           matlab.ui.control.EditField
        yLabel                  matlab.ui.control.Label
        y1515EditField          matlab.ui.control.EditField
        xLabel                  matlab.ui.control.Label
        x010010EditField        matlab.ui.control.EditField
        Tab_6                   matlab.ui.container.Tab
        Button_5                matlab.ui.control.Button
        Button_4                matlab.ui.control.Button
        Button_3                matlab.ui.control.Button
        UIAxes2                 matlab.ui.control.UIAxes
    end

    % Callbacks that handle component events
    methods (Access = private)

        % Button pushed function: Button
        function ButtonPushed(app, event)
             robot = java.awt.Robot(); %创建java.awt.Robot对象robot，自动测试
            rectangle = java.awt.Rectangle(); %创建java.awt.Rectangle对象rectangle，矩形
            rectangle.x = 50; %截图左上角横坐标（屏幕最左上角为原点) 
            rectangle.y = 200;%截图左上角纵坐标（屏幕最左上角为原点) 
            rectangle.width = 600;%截图宽度（屏幕最左上角为原点)
            rectangle.height =600; %截图高度（屏幕最左上角为原点)
            image=robot.createScreenCapture(rectangle); %创建包含从屏幕中读取的像素的图像
            robot.createScreenCapture(rectangle); %创建包含从屏幕中读取的像素的图像
            w=image.getWidth();%获取图像宽度
            h = image.getHeight(); %获取图像高度
            raster =image.getData(); %获取图像RGB数据，返回Raster类的对象
            I= zeros(w*h*3,1); %创建存储RGB像素信息的double数组
            I= raster.getPixels(0,0,w,h,I);%获取图像一维RGB颜色数组
            I= uint8(I);%转换成uint8数据类型
            I1 =I(1:3:length(I)); %提取R色一维数组
            I1=reshape(I1,w,h); %转换为R色二维数组
            l2= I(2:3:length(I));%提取G色一维数组
            l2=reshape(l2,w,h); %转换为G色二维数组
            I3= I(3:3:length(I));%提取B色一维数组
            I3=reshape(I3,w,h); %转换为B色二维数组
            image = uint8(zeros(w,h,3));%创建存储RGB图像信息三维矩阵
            image(1:w,1:h,1)= I1; %导入R色数组
            image(1:w,1:h,2)= l2;%导入G色数组
            image(1:w,1:h,3)= I3;%导入B色数组
            image = imrotate(image,-90,'nearest'); %图像顺时针旋转90度
            image = flipdim(image,2); %图像竖直镜像
            imshow(image);
            [c1,c2]=getpts; %选择颜色点
            c1=ceil(c1); %将选点的位置化为整数
            c2=ceil(c2);
            for i=1:length(c1)
                color(i,:)=image(c2(i),c1(i),:);
            end
            color=double(color);
            color=color/255;
      
            color_get=color;
            color_get1=getappdata(app.UIFigure,'getcolor');
            color_get=[color_get;color_get1];

            app.UITable_2.Data(1:size(color_get,1),1)=(1:size(color_get,1))';
            app.UITable_2.Data(1:size(color_get,1),2)=(1:size(color_get,1))';
%             app.UITable_2.Data(:,1)=(1:size(color_get,1))';
%             app.UITable_2.Data(:,2)=(1:size(color_get,1))';
%             app.UITable_2.BackgroundColor(:,1)=[1,1,1];
            app.UITable_2.BackgroundColor=color_get;
            s = uistyle('BackgroundColor',[1 1 1]);   
            addStyle(app.UITable_2,s,'cell',[(1:size(color_get,1))',ones(size(color_get,1),1)]);
            setappdata(app.UIFigure,'getcolor',color_get);  %后期会引用的数据
     
        end

        % Button pushed function: Button_2
        function Button_2Pushed(app, event)
            load('color_list.mat')
            app.UITable.Data(:,1)=(1:size(color_list,1))';
            app.UITable.Data(:,2)=(1:size(color_list,1))';
%             app.UITable_2.BackgroundColor(:,1)=[1,1,1];
            app.UITable.BackgroundColor=color_list;
            s = uistyle('BackgroundColor',[1 1 1]);
            addStyle(app.UITable,s,'cell',[(1:size(color_list,1))',ones(size(color_list,1),1)]);
        end

        % Value changed function: DropDown
        function DropDownValueChanged(app, event)

        end

        % Button pushed function: Button_3
        function Button_3Pushed(app, event)
             delete (allchild(app.UIAxes2))

            %%
             test_data2=getappdata(app.UIFigure,'shujudata');%总数据
            %Y轴数据导入
          if strcmp(app.DropDown_7.Value,'转置')
              test_data2=test_data2';
          end
            if strcmp(app.DropDown_5.Value,'全部导入')
                test_data1=test_data2;
                yang_num=size(test_data1,1);
                for i=1:yang_num
                    test_data_data=test_data1(i,:);

                   test_data_data(find(isnan(test_data_data)==1))=[];
                    test_ydata{1,i}=test_data_data;
                end
            else
                 y_data1=str2num(app.y23y23EditField.Value);
               test_data1=test_data2(y_data1,:);
                 yang_num=length(y_data1);
                 for i=1:yang_num
                    test_data_data=test_data1(i,:);
                  
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_ydata{1,i}=test_data_data;
                end
            end
            %X轴数据导入
              if (app.xx101lengthyEditField.Value=='0')
                for i=1:yang_num         
                    test_xdata{1,i}=1:length(test_ydata{1,i});
                end
%                   x_data=1:size(test_data1,2);
              elseif (app.xx101lengthyEditField.Value~='0')
                  x_data1=str2num(app.xx101lengthyEditField.Value);
                 x_data=test_data2(x_data1,:); 
                for i=1:length(x_data1)
                    test_data_data=x_data(i,:);
                    
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_xdata{1,i}=test_data_data;
                end
              end
            %%

        % 颜色获取，自取颜色和默认颜色
          load('color_list.mat')
          color_or_label=str2num(app.EditField_4.Value);
          if color_or_label==0
              color_ori=[];
          else
              color_ori=color_list(color_or_label,:);
          end
          color_get=getappdata(app.UIFigure,'getcolor');
          color_ge_label=str2num(app.EditField_5.Value);
           if color_ge_label==0
              color_get1=[];
          else
              color_get1=color_get(color_ge_label,:);
          end
          
          color_all=[color_ori;color_get1];
         if (size(color_all,1)<yang_num)
            for n=size(color_all,1)+1:yang_num
                 color_all(n,:)=color_list(randperm(100,1),:);
%                  [color_all;color_list(randperm(100,10),:)];
            end
%              color_all=[color_all;color_list(randperm(100,10),:)];
         end
         %  线条获取
         Line_Width=str2num(app.EditField_6.Value);
         Line_Width1=1.5*ones(1,yang_num);
         if (length(Line_Width)<yang_num)
             Line_Width=[Line_Width,Line_Width1];
         end
         %线条符号样式获取
        yangsi_str=app.EditField_7.Value;
         yang_str=strsplit(yangsi_str,',');
         yang_str1={'-*','-+','-^','-o','-.','-x','-d','-s','-h','-p'};
         if (length(yang_str)<yang_num)
             for n=length(yang_str)+1:yang_num
             yang_str{1,n}=yang_str1{1,randperm(9,1)};
             end
         end
         makesize=str2num(app.EditField_16.Value);
         if  strcmp( app.DropDown_4.Value,'普通折线图')==1
          for i=1:yang_num
             plot(app.UIAxes2, test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
             hold (app.UIAxes2,'on')
             color_all1=color_all;
          end
         elseif strcmp( app.DropDown_4.Value,'阶梯图')==1
               for i=1:yang_num
             stairs(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
             hold (app.UIAxes2,'on')
             color_all1=color_all;
               end
         elseif strcmp( app.DropDown_4.Value,'误差棒折线图')==1
  %误差上限和下限数据设置
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            elseif length(H_label)==yang_num
                 H_label=H_label;
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             elseif  length(L_label)==yang_num
                 L_label=L_label;
             end
%              disp(length(H_label))
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);
    %    
%       if (strcmp(app.EditField_13.Value,'[0]')~=1)|(strcmp(app.EditField_15.Value,'[0]')~=1)
            color_dai=str2num(app.EditField_13.Value);
            color_dai1=str2num(app.EditField_15.Value);
            if color_dai==0
                color_dai_x=[];
            else
                color_dai_x=color_list(color_dai,:);
            end
             if color_dai1==0
                color_dai_x1=[];
            else
                color_dai_x1=color_get(color_dai1,:);
             end
             color_all1=[color_dai_x;color_dai_x1];
            if size(color_all1,1)<size(color_all,1)
                  
                  color_all1((size(color_all1,1)+1):size(color_all,1),:)=color_all((size(color_all1,1)+1):size(color_all,1),:);
            end
%             else 
%              color_all1=color_all;
%       end
           cap_size=str2num(app.EditField_11.Value); 
           for i=1:yang_num
               errorbar(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},L_data(i,:),H_data(i,:),yang_str{1,i},'Color',color_all1(i,:),'MarkerSize',makesize, 'MarkerEdgeColor',color_all(i,:),'MarkerFaceColor',[1,1,1],...
                'LineWidth', 1.5,'CapSize',cap_size)
             hold (app.UIAxes2,'on')
           end
         elseif strcmp( app.DropDown_4.Value,'误差带折线图')==1
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             end
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);   
%         if ((strcmp(app.EditField_13.Value,'[0]')~=1)||(strcmp(app.EditField_15.Value,'[0]')~=1))
%             disp(111111111)

            color_dai=str2num(app.EditField_13.Value);
            color_dai1=str2num(app.EditField_15.Value);
            if color_dai==0
                color_dai_x=[];
            else
                color_dai_x=color_list(color_dai,:);
            end
             if color_dai1==0
                color_dai1_x1=[];
            else
                color_dai1_x1=color_get(color_dai1,:);
             end
             color_all1=[color_dai_x;color_dai1_x1];
%              disp(color_all1)
            if size(color_all1,1)<size(color_all,1)
                  
                  color_all1((size(color_all1,1)+1):size(color_all,1),:)=color_all((size(color_all1,1)+1):size(color_all,1),:);
            end
%        else 
%                color_all1=color_all;
%               
%      end
             %误差带颜色
         color_all_bian=color_all1;
             for i=1:yang_num
             h1=fill(app.UIAxes2,[test_xdata{1,i},fliplr(test_xdata{1,i})],[test_ydata{1,i}-L_data(i,:),fliplr(test_ydata{1,i}+H_data(i,:))],'r');
             hold (app.UIAxes2,'on')
             h1.FaceColor = color_all1(i,:);%定义区间的填充颜色      
             h1.EdgeColor =[1,1,1];%边界颜色设置为白色
%             set(h1,'alphadata',0.2)
%             h1.AlphaData = 0.2; 
             alpha (app.UIAxes2,0.3)   %设置透明色
            plot(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i),'MarkerSize',makesize) 
             end
         end
          value1=app.DropDown_2.Value;
          kuang_width=str2num(app.EditField_17.Value);
          if strcmp(value1,'默认')==1
              set(app.UIAxes2,"FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'新罗马')==1
              set(app.UIAxes2,"FontName","Times New Roman","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'宋体')==1
             set(app.UIAxes2,"FontName","宋体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'黑体')==1
             set(app.UIAxes2,"FontName","黑体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'楷体')==1
             set(app.UIAxes2,"FontName","楷体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'简雅黑')==1
             set(app.UIAxes2,"FontName","简雅黑","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          end
        hold (app.UIAxes2,'on')
          legend_str=app.EditField_8.Value;
          xlabel(app.UIAxes2,app.xEditField.Value)
          ylabel(app.UIAxes2,app.yEditField.Value)
          title(app.UIAxes2,app.EditField.Value)
          legend(app.UIAxes2,strsplit(legend_str,','))
                     if (strcmp(app.DropDown_9.Value,'半框')==1)
              box(app.UIAxes2,"off")
          else
             box(app.UIAxes2,"on")  

          end

           if (strcmp(app.DropDown_10.Value,'无框')==1)
                legend(app.UIAxes2,'boxoff') %图例框消失
          else
                legend(app.UIAxes2,'boxon') %图例框消失
           end
           
          if (strcmp(app.DropDown_8.Value,'开')==1)
             grid(app.UIAxes2,"on")
          elseif (strcmp(app.DropDown_8.Value,'半开')==1)
              grid(app.UIAxes2,"minor")
          else
               grid(app.UIAxes2,"off")
          end
         % 细微设置
      if (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')==1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
            if  (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
%             set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.xA1A2EditField.Value,',');
 
            elseif (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')~=1)
               XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%               app.UIAxes2.XTick=[XSim_value];
            end

        elseif (strcmp(app.y1515EditField.Value,'0')~=1)&(strcmp(app.x010010EditField.Value,'0')==1)
               YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
             
            if  (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
             YSim_value=str2num(app.y12100EditField.Value);
             set(app.UIAxes2,'YTick',YSim_value)
            set(app.UIAxes2,'XTickLabel',strsplit(app.yEditField_2.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.yEditField_2.Value,',');
 
            elseif (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
               YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YSim_value)

            end

        elseif (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')~=1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
                YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
                if (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YSim_value)
                    if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')==1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                 YSim_value=str2num(app.y12100EditField.Value);
                 set(app.UIAxes2,'YTick',YSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                end
          end
           hold (app.UIAxes2,'on')

            if (app.xA1A2EditField.Value~='0')
            set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%                app.UIAxes2.XTickLabel=strsplit(app.xA1A2EditField.Value,',');
            end
           if (app.yEditField_2.Value~='0')
             set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
%                app.UIAxes2.YTickLabel=strsplit(app.yEditField_2.Value,',');
            end
         %细微设置
         setappdata(app.UIFigure,'yang_data',yang_str);  %后期会引用的数据
         setappdata(app.UIFigure,'color_data',color_all);  %后期会引用的数据
         setappdata(app.UIFigure,'color_data1',color_all1);  %后期会引用的数据
%          setappdata(app.UIFigure,'color_data1',color_all1);  %后期会引用的数据
        end

        % Button pushed function: Button_4
        function Button_4Pushed(app, event)
                  delete (allchild(app.UIAxes2))
     test_data2=getappdata(app.UIFigure,'shujudata');%总数据
            %Y轴数据导入
          if strcmp(app.DropDown_7.Value,'转置')
              test_data2=test_data2';
          end
            if strcmp(app.DropDown_5.Value,'全部导入')
                test_data1=test_data2;
                yang_num=size(test_data1,1);
                for i=1:yang_num
                    test_data_data=test_data1(i,:);

                   test_data_data(find(isnan(test_data_data)==1))=[];
                    test_ydata{1,i}=test_data_data;
                end
            else
                 y_data1=str2num(app.y23y23EditField.Value);
               test_data1=test_data2(y_data1,:);
                 yang_num=length(y_data1);
                 for i=1:yang_num
                    test_data_data=test_data1(i,:);
                  
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_ydata{1,i}=test_data_data;
                end
            end
            %X轴数据导入
              if (app.xx101lengthyEditField.Value=='0')
                for i=1:yang_num         
                    test_xdata{1,i}=1:length(test_ydata{1,i});
                end
%                   x_data=1:size(test_data1,2);
              elseif (app.xx101lengthyEditField.Value~='0')
                  x_data1=str2num(app.xx101lengthyEditField.Value);
                 x_data=test_data2(x_data1,:); 
                for i=1:length(x_data1)
                    test_data_data=x_data(i,:);
                    
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_xdata{1,i}=test_data_data;
                end
              end
        % 颜色获取，自取颜色和默认颜色
                 % 颜色获取
          load('color_list.mat')
          % color_list
         %  线条获取
           Line_Width=str2num(app.EditField_6.Value);
         Line_Width1=[1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5];
         if (length(Line_Width)<yang_num)
             Line_Width=[Line_Width,Line_Width1];
         end
        color_list_cha=color_list(:,1)*0.299+color_list(:,2)*0.587+color_list(:,3)*0.114;
        color_list_index=find(color_list_cha*255<180);
        color_list=color_list(color_list_index,:);
%          yang_fu1={'-*','-+','-^','-o','-.','-x','-d','-s','-h','-p','-|','-v','->','--<','--*','--+','--^','--o','--.','--x','--d','--s','--h','--p','--|','--v','-->','--<',...
%              '*','+','^','o','.','x','d','s','h','p','|','v','>','<',':*',':+',':^',':o',':.',':x',':d',':s',':h',':p',':|',':v',':>',':<'};
         yang_fu1={'*','+','^','o','.','x','d','s','h','p','|','v','>','<',''};
         yang_fu2={'-','--','-',':','-',':','--','-','--','-',':'};
%           yang_str1={'*','+','^','o','.','x','d','s','h','p','|','v','>','<'}
          rand_list1=randperm(length(color_list),yang_num);
          rand_list2=randperm(length(yang_fu1),yang_num);

%           for i=1:length(y_data1)
%               yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
%              plot(app.UIAxes2,x_data,test_data(y_data1(i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
%              hold (app.UIAxes2,'on')
%              cell_str{1,i}=yang_str1;
%           end
              makesize=str2num(app.EditField_16.Value);

         if  strcmp( app.DropDown_4.Value,'普通折线图')==1 
          for i=1:yang_num
             yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             plot(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
             cell_str{1,i}=yang_str1;
%              plot(app.UIAxes2,x_data,test_data((i),:),yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i))
             hold (app.UIAxes2,'on')
          end
          elseif strcmp( app.DropDown_4.Value,'阶梯图')==1
               for i=1:yang_num
              yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             stairs(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
             hold (app.UIAxes2,'on')
%              color_all1=color_all;
             cell_str{1,i}=yang_str1;
              end
         elseif strcmp( app.DropDown_4.Value,'误差棒折线图')==1
  %误差上限和下限数据设置
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            elseif length(H_label)==yang_num
                 H_label=H_label;
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             elseif  length(L_label)==yang_num
                 L_label=L_label;
             end
%              disp(length(H_label))
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);

           cap_size=str2num(app.EditField_11.Value); 
           for i=1:yang_num
                 yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
                cell_str{1,i}=yang_str1;
               errorbar(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},L_data(i,:),H_data(i,:),yang_str1,'Color',color_list(rand_list1(i),:),'MarkerSize',makesize, 'MarkerEdgeColor',color_list(rand_list1(i),:),'MarkerFaceColor',[1,1,1],...
                'LineWidth', 1.5,'CapSize',cap_size)
%                errorbar(app.UIAxes2,x_data,test_data((i),:),L_data(i,:),H_data(i,:),yang_str{1,i},'Color',color_all1(i,:),'MarkerSize',10, 'MarkerEdgeColor',color_all(i,:),'MarkerFaceColor',[1,1,1],...
%                 'LineWidth', 1.5,'CapSize',cap_size)
             hold (app.UIAxes2,'on')
           end
         elseif strcmp( app.DropDown_4.Value,'误差带折线图')==1
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             end
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);   
             %误差带颜色
             yang_fu2={'-','--','-',':','-','-','-','-','-',':'};
             
             for i=1:yang_num
                 yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
%              plot(app.UIAxes2,x_data,test_data((i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
             cell_str{1,i}=yang_str1;
                h1=fill(app.UIAxes2,[test_xdata{1,i},fliplr(test_xdata{1,i})],[test_ydata{1,i}-L_data(i,:),fliplr(test_ydata{1,i}+H_data(i,:))],'r');
             hold (app.UIAxes2,'on')
             h1.FaceColor = color_list(rand_list1(i),:);%定义区间的填充颜色      
             h1.EdgeColor =[1,1,1];%边界颜色设置为白色
%             set(h1,'alphadata',0.2)
%             h1.AlphaData = 0.2; 
             alpha (app.UIAxes2,0.3)   %设置透明色
            plot(app.UIAxes2,test_xdata{1,i}, test_ydata{1,i},yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize) 
             end
         end
          value1=app.DropDown_2.Value;
          kuang_width=str2num(app.EditField_17.Value);
          if strcmp(value1,'默认')==1
              set(app.UIAxes2,"FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'新罗马')==1
              set(app.UIAxes2,"FontName","Times New Roman","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'宋体')==1
             set(app.UIAxes2,"FontName","宋体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'黑体')==1
             set(app.UIAxes2,"FontName","黑体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'楷体')==1
             set(app.UIAxes2,"FontName","楷体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'简雅黑')==1
             set(app.UIAxes2,"FontName","简雅黑","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          end
        hold (app.UIAxes2,'on')
          legend_str=app.EditField_8.Value;
          xlabel(app.UIAxes2,app.xEditField.Value)
          ylabel(app.UIAxes2,app.yEditField.Value)
          title(app.UIAxes2,app.EditField.Value)
          legend(app.UIAxes2,strsplit(legend_str,','))
         if (strcmp(app.DropDown_9.Value,'半框')==1)
             box(app.UIAxes2,"off")
          else
             box(app.UIAxes2,"on")  

         end

           if (strcmp(app.DropDown_10.Value,'无框')==1)
                legend(app.UIAxes2,'boxoff') %图例框消失
          else
                legend(app.UIAxes2,'boxon') %图例框消失
          end


          if (strcmp(app.DropDown_8.Value,'开')==1)
             grid(app.UIAxes2,"on")
          elseif (strcmp(app.DropDown_8.Value,'半开')==1)
              grid(app.UIAxes2,"minor")
          else
               grid(app.UIAxes2,"off")
          end
         % 细微设置
      if (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')==1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
            if  (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
%             set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.xA1A2EditField.Value,',');
 
            elseif (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')~=1)
               XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%               app.UIAxes2.XTick=[XSim_value];
            end

        elseif (strcmp(app.y1515EditField.Value,'0')~=1)&(strcmp(app.x010010EditField.Value,'0')==1)
               YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
             
            if  (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
             YSim_value=str2num(app.y12100EditField.Value);
             set(app.UIAxes2,'YTick',YSim_value)
            set(app.UIAxes2,'XTickLabel',strsplit(app.yEditField_2.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.yEditField_2.Value,',');
 
            elseif (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
               YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YSim_value)

            end

        elseif (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')~=1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
                YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
                if (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YSim_value)
                    if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')==1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                 YSim_value=str2num(app.y12100EditField.Value);
                 set(app.UIAxes2,'YTick',YSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                end
          end
 
         %细微设置
         setappdata(app.UIFigure,'yang_data',cell_str);  %后期会引用的数据
         setappdata(app.UIFigure,'color_data',color_list((rand_list1),:));  %后期会引用的数据
         setappdata(app.UIFigure,'color_data1',color_list((rand_list1),:));  %后期会引用的数据
%          setappdata(app.UIFigure,'color_data1',color_all1);  %后期会引用的数据
          
          
        end

        % Button pushed function: Button_7
        function Button_7Pushed(app, event)
            close all
       test_data2=getappdata(app.UIFigure,'shujudata');%总数据
            %Y轴数据导入
          if strcmp(app.DropDown_7.Value,'转置')
              test_data2=test_data2';
          end
            if strcmp(app.DropDown_5.Value,'全部导入')
                test_data1=test_data2;
                yang_num=size(test_data1,1);
                for i=1:yang_num
                    test_data_data=test_data1(i,:);

                   test_data_data(find(isnan(test_data_data)==1))=[];
                    test_ydata{1,i}=test_data_data;
                end
            else
                 y_data1=str2num(app.y23y23EditField.Value);
               test_data1=test_data2(y_data1,:);
                 yang_num=length(y_data1);
                 for i=1:yang_num
                    test_data_data=test_data1(i,:);
                  
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_ydata{1,i}=test_data_data;
                end
            end
            %X轴数据导入
              if (app.xx101lengthyEditField.Value=='0')
                for i=1:yang_num         
                    test_xdata{1,i}=1:length(test_ydata{1,i});
                end
%                   x_data=1:size(test_data1,2);
              elseif (app.xx101lengthyEditField.Value~='0')
                  x_data1=str2num(app.xx101lengthyEditField.Value);
                 x_data=test_data2(x_data1,:); 
                for i=1:length(x_data1)
                    test_data_data=x_data(i,:);
                    
                        test_data_data(find(isnan(test_data_data)==1))=[];
                   
                    test_xdata{1,i}=test_data_data;
                end
              end
         
         %图窗大小
           len_low=str2num(app.cm8cm128EditField.Value);
           danwei=app.DropDown_3.Value;
         
          figure('Units', danwei, ...
         'Position', [5 5 len_low(1) len_low(2)]);
           Line_Width=str2num(app.EditField_6.Value);
         Line_Width1=[1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5];
         if (length(Line_Width)<yang_num)
             Line_Width=[Line_Width,Line_Width1];
         end
          ax = gca;
         %
          yang_str=getappdata(app.UIFigure,'yang_data');
         color_list=getappdata(app.UIFigure,'color_data');
         color_list1=getappdata(app.UIFigure,'color_data1');
              makesize=str2num(app.EditField_16.Value);
%          if  strcmp( app.DropDown_4.Value,'普通折线图')==1
%           for i=1:yang_num
%              plot(app.UIAxes2,x_data,test_data((i),:),yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
%              hold (app.UIAxes2,'on')
%              color_all1=color_all;
%           end
          if strcmp( app.DropDown_4.Value,'普通折线图')==1 
          for i=1:yang_num
%              yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             plot(gca,test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_list((i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
%              cell_str{1,i}=yang_str1;
%              plot(gca,x_data,test_data((i),:),yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i))
             hold (gca,'on')
          end
            elseif strcmp( app.DropDown_4.Value,'阶梯图')==1
               for i=1:yang_num
%   yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             stairs(gca,test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_list((i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize)
             hold (gca,'on')
%              color_all1=color_all;
              end
         elseif strcmp( app.DropDown_4.Value,'误差棒折线图')==1
  %误差上限和下限数据设置
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            elseif length(H_label)==yang_num
                 H_label=H_label;
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             elseif  length(L_label)==yang_num
                 L_label=L_label;
             end
%              disp(length(H_label))
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);

           cap_size=str2num(app.EditField_11.Value); 
           for i=1:yang_num
%                  yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
               
               errorbar(gca,test_xdata{1,i}, test_ydata{1,i},L_data(i,:),H_data(i,:),yang_str{1,i},'Color',color_list((i),:),'MarkerSize',makesize, 'MarkerEdgeColor',color_list1((i),:),'MarkerFaceColor',[1,1,1],...
                'LineWidth', 1.5,'CapSize',cap_size)
%                errorbar(gca,x_data,test_data((i),:),L_data(i,:),H_data(i,:),yang_str{1,i},'Color',color_all1(i,:),'MarkerSize',10, 'MarkerEdgeColor',color_all(i,:),'MarkerFaceColor',[1,1,1],...
%                 'LineWidth', 1.5,'CapSize',cap_size)
             hold (gca,'on')
           end
         elseif strcmp( app.DropDown_4.Value,'误差带折线图')==1
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             end
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);   
             %误差带颜色

             for i=1:yang_num
               h1=fill(gca,[test_xdata{1,i},fliplr(test_xdata{1,i})],[test_ydata{1,i}-L_data(i,:),fliplr(test_ydata{1,i}+H_data(i,:))],'r');
             hold (gca,'on')
             h1.FaceColor = color_list1((i),:);%定义区间的填充颜色      
             h1.EdgeColor =[1,1,1];%边界颜色设置为白色
%             set(h1,'alphadata',0.2)
%             h1.AlphaData = 0.2; 
             alpha (gca,0.3)   %设置透明色
            plot(gca,test_xdata{1,i}, test_ydata{1,i},yang_str{1,i},'Color',color_list((i),:),'LineWidth',Line_Width(i),'MarkerSize',makesize) 
             end
         end
          value1=app.DropDown_2.Value;
          kuang_width=str2num(app.EditField_17.Value);
          if strcmp(value1,'默认')==1
              set(gca,"FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'新罗马')==1
              set(gca,"FontName","Times New Roman","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'宋体')==1
             set(gca,"FontName","宋体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'黑体')==1
             set(gca,"FontName","黑体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'楷体')==1
             set(gca,"FontName","楷体","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          elseif strcmp(value1,'简雅黑')==1
             set(gca,"FontName","简雅黑","FontSize",str2num(app.EditField_3.Value),"LineWidth",kuang_width)
          end
        hold (gca,'on')
          legend_str=app.EditField_8.Value;
          xlabel(gca,app.xEditField.Value)
          ylabel(gca,app.yEditField.Value)
          title(gca,app.EditField.Value)
          legend(gca,strsplit(legend_str,','))
            if (strcmp(app.DropDown_9.Value,'半框')==1)
              box(gca,"off")
          else
             box(gca,"on")  

              end

          if (strcmp(app.DropDown_10.Value,'无框')==1)
                legend(gca,'boxoff') %图例框消失
          else
                legend(gca,'boxon') %图例框消失
          end
          
          if (strcmp(app.DropDown_8.Value,'开')==1)
             grid(gca,"on")
          elseif (strcmp(app.DropDown_8.Value,'半开')==1)
              grid(gca,"minor")
          else
               grid(gca,"off")
          end
         % 细微设置
             if (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')==1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(gca,'XLim',[XLim_value(1),XLim_value(2)])
            if  (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(gca,'XTick',XSim_value)
%             set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%             gca.XTickLabel=strsplit(app.xA1A2EditField.Value,',');
 
            elseif (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')~=1)
               XSim_value=str2num(app.x134EditField.Value);
                set(gca,'XTick',XSim_value)
                set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%               gca.XTick=[XSim_value];
            end

        elseif (strcmp(app.y1515EditField.Value,'0')~=1)&(strcmp(app.x010010EditField.Value,'0')==1)
               YLim_value=str2num(app.y1515EditField.Value);
               set(gca,'YLim',[YLim_value(1),YLim_value(2)])
             
            if  (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
             YSim_value=str2num(app.y12100EditField.Value);
             set(gca,'YTick',YSim_value)
            set(gca,'XTickLabel',strsplit(app.yEditField_2.Value,','))
%             gca.XTickLabel=strsplit(app.yEditField_2.Value,',');
 
            elseif (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
               YSim_value=str2num(app.y12100EditField.Value);
                set(gca,'YTick',YSim_value)

            end

        elseif (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')~=1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(gca,'XLim',[XLim_value(1),XLim_value(2)])
                YLim_value=str2num(app.y1515EditField.Value);
               set(gca,'YLim',[YLim_value(1),YLim_value(2)])
                if (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                XSim_value=str2num(app.x134EditField.Value);
                set(gca,'XTick',XSim_value)
                YSim_value=str2num(app.y12100EditField.Value);
                set(gca,'YTick',YSim_value)
                    if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')==1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                 YSim_value=str2num(app.y12100EditField.Value);
                 set(gca,'YTick',YSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(gca,'XTick',XSim_value)
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(gca,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(gca,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                end
          end

%           box off
%           legend('boxoff') %图例框消失
        end

        % Button pushed function: Button_9
        function Button_9Pushed(app, event)
             value = app.DropDown.Value;
            if strcmp(value,'mat数据')==1
                [filename,pathname]=uigetfile({'*.mat'});
                data_str=strcat(pathname,filename);
                data=cell2mat(struct2cell(load(data_str)));
           elseif strcmp(value,'excel数据')==1
                [filename,pathname]=uigetfile({'*.xlsx'});
                data_str=strcat(pathname,filename);
                data=xlsread(data_str);
            end
            setappdata(app.UIFigure,'shujudata',data);  %后期会引用的数据
        end

        % Button pushed function: Button_8
        function Button_8Pushed(app, event)
            magnifyOnFigure;
        end

        % Button pushed function: Button_5
        function Button_5Pushed(app, event)

                                   delete (allchild(app.UIAxes2))
            test_data2=getappdata(app.UIFigure,'shujudata');%总数据
            %Y轴数据导入
               if strcmp(app.DropDown_7.Value,'转置')
              test_data2=test_data2';
          end
            if strcmp(app.DropDown_5.Value,'全部导入')
                test_data1=test_data2;
                yang_num=size(test_data1,1);
            else
                 y_data1=str2num(app.y23y23EditField.Value);
               test_data1=test_data2(y_data1,:);
                 yang_num=length(y_data1);
            end
            %X轴数据导入
              if (app.xx101lengthyEditField.Value=='0')
                  x_data=1:size(test_data1,2);
              elseif (app.xx101lengthyEditField.Value~='0')
                  x_data1=str2num(app.xx101lengthyEditField.Value);
                 x_data=test_data2(x_data1,:);                
              end

           test_data=test_data1;
          num=str2num(app.DropDown_11.Value(end));
            str=['图片导入/折线图导入/',num2str(num),'.jpeg'];
            hua=imread(str);
            % figure(1)
            % imshow(hua);
            M=size(hua,1);
            N=size(hua,2);
            L1=1:20:M;
            L2=1:20:N;
            juzheng=[];
            for i=1:length(L1)
                for j=1:length(L2)
                    juzheng((i-1)*(length(L2))+j,1)=L1(i);
                    juzheng((i-1)*(length(L2))+j,2)=L2(j);
                end
            end
            % color_list=[];
            for i=1:length(juzheng)
                  color_list(i,:)=hua(juzheng(i,1),juzheng(i,2),:);
            end
            
            color_list=double(color_list);
            color_label=color_list(:,1)*0.299+color_list(:,2)*0.587+color_list(:,3)*0.114;
            color_label_U=unique(color_label);
            color_all_index=[];
            for i=1:length(color_label_U)
                color_all_index{1,i}=find(color_label==color_label_U(i));
                color_all_index1(i)=color_all_index{1,i}(1);
            end
            color_all_need=color_list(color_all_index1,:);
            color_all_need_label=color_all_need(:,1)*0.299+color_all_need(:,2)*0.587+color_all_need(:,3)*0.114;
            color_all_need_label_index=find((color_all_need_label>50)&(color_all_need_label<230));
            color_all1=color_all_need(color_all_need_label_index,:);
            
            % ju_num=randi([6,10]);
%              ju_num=str2num(app.EditField_15.Value);
            [~,C]=kmeans(color_all1,yang_num+2);
            C_label=(C(:,1)*0.299+C(:,2)*0.587+C(:,3)*0.114);
            [~,color_all_need_label_index1]=sort(C_label);
            % [~,color_all_need_label_index2]=sort(color_all_need_label_index1,'descend');
            color_all1=C(color_all_need_label_index1,:);
            color_list=color_all1(1:end-2,:)/255;
          % color_list
         %  线条获取
           Line_Width=str2num(app.EditField_6.Value);
         Line_Width1=[1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5];
         if (length(Line_Width)<yang_num)
             Line_Width=[Line_Width,Line_Width1];
         end
        color_list_cha=color_list(:,1)*0.299+color_list(:,2)*0.587+color_list(:,3)*0.114;
        color_list_index=find(color_list_cha*255<180);
        color_list=color_list(color_list_index,:);
%          yang_fu1={'-*','-+','-^','-o','-.','-x','-d','-s','-h','-p','-|','-v','->','--<','--*','--+','--^','--o','--.','--x','--d','--s','--h','--p','--|','--v','-->','--<',...
%              '*','+','^','o','.','x','d','s','h','p','|','v','>','<',':*',':+',':^',':o',':.',':x',':d',':s',':h',':p',':|',':v',':>',':<'};
         yang_fu1={'*','+','^','o','x','d','s','h','p','|','v','>','<','','*','+','^','o','x','d','s','h','p','|','v','>','<',''};
         yang_fu2={'-','--','-',':','-','--','--','-','--','-','',':','-','--','-',':','-','--','--','-','--','-','',':'};
%           yang_str1={'*','+','^','o','.','x','d','s','h','p','|','v','>','<'}
          rand_list1=1:yang_num;
          rand_list2=1:yang_num;

%           for i=1:length(y_data1)
%               yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
%              plot(app.UIAxes2,x_data,test_data(y_data1(i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
%              hold (app.UIAxes2,'on')
%              cell_str{1,i}=yang_str1;
%           end
          
                 if  strcmp( app.DropDown_4.Value,'普通折线图')==1 
          for i=1:yang_num
             yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             plot(app.UIAxes2,x_data,test_data((i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
             cell_str{1,i}=yang_str1;
%              plot(app.UIAxes2,x_data,test_data((i),:),yang_str{1,i},'Color',color_all(i,:),'LineWidth',Line_Width(i))
             hold (app.UIAxes2,'on')
          end
          elseif strcmp( app.DropDown_4.Value,'阶梯图')==1
               for i=1:yang_num
              yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
             stairs(app.UIAxes2,x_data,test_data((i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
             hold (app.UIAxes2,'on')
%              color_all1=color_all;
             cell_str{1,i}=yang_str1;
              end
         elseif strcmp( app.DropDown_4.Value,'误差棒折线图')==1
  %误差上限和下限数据设置
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            elseif length(H_label)==yang_num
                 H_label=H_label;
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             elseif  length(L_label)==yang_num
                 L_label=L_label;
             end
%              disp(length(H_label))
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);

           cap_size=str2num(app.EditField_11.Value); 
           for i=1:yang_num
                 yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
                cell_str{1,i}=yang_str1;
               errorbar(app.UIAxes2,x_data,test_data((i),:),L_data(i,:),H_data(i,:),yang_str1,'Color',color_list(rand_list1(i),:),'MarkerSize',10, 'MarkerEdgeColor',color_list(rand_list1(i),:),'MarkerFaceColor',[1,1,1],...
                'LineWidth', 1.5,'CapSize',cap_size)
%                errorbar(app.UIAxes2,x_data,test_data((i),:),L_data(i,:),H_data(i,:),yang_str{1,i},'Color',color_all1(i,:),'MarkerSize',10, 'MarkerEdgeColor',color_all(i,:),'MarkerFaceColor',[1,1,1],...
%                 'LineWidth', 1.5,'CapSize',cap_size)
             hold (app.UIAxes2,'on')
           end
         elseif strcmp( app.DropDown_4.Value,'误差带折线图')==1
             H_label=str2num(app.EditField_9.Value); %上限 label
             L_label=str2num(app.EditField_10.Value); %下限 label
            if length(H_label)<yang_num
                 H_label=[H_label,H_label(1)*ones(1,yang_num-length(H_label))];
            elseif length(H_label)>yang_num
                H_label=H_label(1:yang_num);
            end

             if length(L_label)<yang_num
                 L_label=[L_label,L_label(1)*ones(1,yang_num-length(L_label))];
            elseif length(L_label)>yang_num
                 L_label=L_label(1:yang_num);
             end
             H_data=test_data2(H_label,:);
             L_data=test_data2(L_label,:);   
             %误差带颜色
             yang_fu2={'-','--','-',':','-','-','-','-','-',':'};
             
             for i=1:yang_num
                 yang_str1=[yang_fu2{1,randperm(length(yang_fu2),1)},yang_fu1{1,rand_list2(i)}];
%              plot(app.UIAxes2,x_data,test_data((i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',Line_Width(i))
             cell_str{1,i}=yang_str1;
             h1=fill(app.UIAxes2,[x_data,fliplr(x_data)],[test_data((i),:)-L_data(i,:),fliplr(H_data(i,:)+test_data((i),:))],'r');
             hold (app.UIAxes2,'on')
             h1.FaceColor = color_list(rand_list1(i),:);%定义区间的填充颜色      
             h1.EdgeColor =[1,1,1];%边界颜色设置为白色
%             set(h1,'alphadata',0.2)
%             h1.AlphaData = 0.2; 
             alpha (app.UIAxes2,0.3)   %设置透明色
            plot(app.UIAxes2,x_data,test_data((i),:),yang_str1,'Color',color_list(rand_list1(i),:),'LineWidth',2,'DisplayName','prediction') 
             end
         end
          value1=app.DropDown_2.Value;
          if strcmp(value1,'默认')==1
              set(app.UIAxes2,"FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          elseif strcmp(value1,'新罗马')==1
              set(app.UIAxes2,"FontName","Times New Roman","FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          elseif strcmp(value1,'宋体')==1
             set(app.UIAxes2,"FontName","宋体","FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          elseif strcmp(value1,'黑体')==1
             set(app.UIAxes2,"FontName","黑体","FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          elseif strcmp(value1,'楷体')==1
             set(app.UIAxes2,"FontName","楷体","FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          elseif strcmp(value1,'简雅黑')==1
             set(app.UIAxes2,"FontName","简雅黑","FontSize",str2num(app.EditField_3.Value),"LineWidth",1)
          end
        hold (app.UIAxes2,'on')
          legend_str=app.EditField_8.Value;
          xlabel(app.UIAxes2,app.xEditField.Value)
          ylabel(app.UIAxes2,app.yEditField.Value)
          title(app.UIAxes2,app.EditField.Value)
          legend(app.UIAxes2,strsplit(legend_str,','))
         if (strcmp(app.DropDown_9.Value,'半框')==1)
             box(app.UIAxes2,"off")
          else
             box(app.UIAxes2,"on")  

         end

           if (strcmp(app.DropDown_10.Value,'无框')==1)
                legend(app.UIAxes2,'boxoff') %图例框消失
          else
                legend(app.UIAxes2,'boxon') %图例框消失
          end


          if (strcmp(app.DropDown_8.Value,'开')==1)
             grid(app.UIAxes2,"on")
          elseif (strcmp(app.DropDown_8.Value,'半开')==1)
              grid(app.UIAxes2,"minor")
          else
               grid(app.UIAxes2,"off")
          end
         % 细微设置
          if (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')==1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
            if  (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XLim_value(1):XSim_value:XLim_value(2))
%             set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.xA1A2EditField.Value,',');
 
            elseif (strcmp(app.x134EditField.Value,'0')~=1)&(strcmp(app.xA1A2EditField.Value,'0')~=1)
               XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XLim_value(1):XSim_value:XLim_value(2))
                set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
%               app.UIAxes2.XTick=[XLim_value(1):XSim_value:XLim_value(2)];
            end

        elseif (strcmp(app.y1515EditField.Value,'0')~=1)&(strcmp(app.x010010EditField.Value,'0')==1)
               YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
             
            if  (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
             YSim_value=str2num(app.y12100EditField.Value);
             set(app.UIAxes2,'YTick',YLim_value(1):YSim_value:YLim_value(2))
            set(app.UIAxes2,'XTickLabel',strsplit(app.yEditField_2.Value,','))
%             app.UIAxes2.XTickLabel=strsplit(app.yEditField_2.Value,',');
 
            elseif (strcmp(app.y12100EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
               YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YLim_value(1):YSim_value:YLim_value(2))

            end

        elseif (strcmp(app.x010010EditField.Value,'0')~=1)&(strcmp(app.y1515EditField.Value,'0')~=1)
               XLim_value=str2num(app.x010010EditField.Value);
               set(app.UIAxes2,'XLim',[XLim_value(1),XLim_value(2)])
                YLim_value=str2num(app.y1515EditField.Value);
               set(app.UIAxes2,'YLim',[YLim_value(1),YLim_value(2)])
                if (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XLim_value(1):XSim_value:XLim_value(2))
                YSim_value=str2num(app.y12100EditField.Value);
                set(app.UIAxes2,'YTick',YLim_value(1):YSim_value:YLim_value(2))
                    if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')==1)&&(strcmp(app.y12100EditField.Value,'0')~=1)
                 YSim_value=str2num(app.y12100EditField.Value);
                 set(app.UIAxes2,'YTick',YLim_value(1):YSim_value:YLim_value(2))
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                elseif (strcmp(app.x134EditField.Value,'0')~=1)&&(strcmp(app.y12100EditField.Value,'0')==1)
                XSim_value=str2num(app.x134EditField.Value);
                set(app.UIAxes2,'XTick',XLim_value(1):XSim_value:XLim_value(2))
                if (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                         set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                         set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')~=1)&(strcmp(app.yEditField_2.Value,'0')==1)
                        set(app.UIAxes2,'XTickLabel',strsplit(app.xA1A2EditField.Value,','))
                    elseif (strcmp(app.xA1A2EditField.Value,'0')==1)&(strcmp(app.yEditField_2.Value,'0')~=1)
                        set(app.UIAxes2,'YTickLabel',strsplit(app.yEditField_2.Value,','))
                    end
                end
          end
 
         %细微设置
         setappdata(app.UIFigure,'yang_data',cell_str);  %后期会引用的数据
         setappdata(app.UIFigure,'color_data',color_list((rand_list1),:));  %后期会引用的数据
         setappdata(app.UIFigure,'color_data1',color_list((rand_list1),:));  %后期会引用的数据
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Color = [0.9412 0.9412 0.9412];
            app.UIFigure.Position = [100 100 914 723];
            app.UIFigure.Name = 'MATLAB App';

            % Create TabGroup
            app.TabGroup = uitabgroup(app.UIFigure);
            app.TabGroup.Position = [1 0 676 724];

            % Create Tab
            app.Tab = uitab(app.TabGroup);
            app.Tab.Title = '折线图';
            app.Tab.BackgroundColor = [0.9176 0.9412 0.9137];

            % Create UIAxes2
            app.UIAxes2 = uiaxes(app.Tab);
            title(app.UIAxes2, 'Title')
            xlabel(app.UIAxes2, 'X')
            ylabel(app.UIAxes2, 'Y')
            zlabel(app.UIAxes2, 'Z')
            app.UIAxes2.Position = [239 291 427 368];

            % Create Button_3
            app.Button_3 = uibutton(app.Tab, 'push');
            app.Button_3.ButtonPushedFcn = createCallbackFcn(app, @Button_3Pushed, true);
            app.Button_3.FontSize = 14;
            app.Button_3.FontWeight = 'bold';
            app.Button_3.FontColor = [0.3725 0.5294 0.1647];
            app.Button_3.Position = [416 668 100 26];
            app.Button_3.Text = '更新图片';

            % Create Button_4
            app.Button_4 = uibutton(app.Tab, 'push');
            app.Button_4.ButtonPushedFcn = createCallbackFcn(app, @Button_4Pushed, true);
            app.Button_4.FontSize = 14;
            app.Button_4.FontWeight = 'bold';
            app.Button_4.FontColor = [0.2706 0.4588 0.0196];
            app.Button_4.Position = [530 266 100 26];
            app.Button_4.Text = '随机美化';

            % Create Button_5
            app.Button_5 = uibutton(app.Tab, 'push');
            app.Button_5.ButtonPushedFcn = createCallbackFcn(app, @Button_5Pushed, true);
            app.Button_5.FontSize = 14;
            app.Button_5.FontWeight = 'bold';
            app.Button_5.FontColor = [0.2706 0.4588 0.0196];
            app.Button_5.Position = [261 266 100 26];
            app.Button_5.Text = '经典美化';

            % Create TabGroup2
            app.TabGroup2 = uitabgroup(app.Tab);
            app.TabGroup2.Position = [1 101 232 328];

            % Create Tab_4
            app.Tab_4 = uitab(app.TabGroup2);
            app.Tab_4.Title = '标签设置';
            app.Tab_4.BackgroundColor = [1 1 1];

            % Create xEditField
            app.xEditField = uieditfield(app.Tab_4, 'text');
            app.xEditField.FontWeight = 'bold';
            app.xEditField.Position = [77 270 132 22];
            app.xEditField.Value = 'X';

            % Create xEditFieldLabel
            app.xEditFieldLabel = uilabel(app.Tab_4);
            app.xEditFieldLabel.FontWeight = 'bold';
            app.xEditFieldLabel.Position = [16 270 48 22];
            app.xEditFieldLabel.Text = 'x轴坐标';

            % Create yEditField
            app.yEditField = uieditfield(app.Tab_4, 'text');
            app.yEditField.FontWeight = 'bold';
            app.yEditField.Position = [77 239 132 22];
            app.yEditField.Value = 'Y';

            % Create yEditFieldLabel
            app.yEditFieldLabel = uilabel(app.Tab_4);
            app.yEditFieldLabel.FontWeight = 'bold';
            app.yEditFieldLabel.Position = [16 239 48 22];
            app.yEditFieldLabel.Text = 'y轴坐标';

            % Create EditField
            app.EditField = uieditfield(app.Tab_4, 'text');
            app.EditField.FontWeight = 'bold';
            app.EditField.Position = [77 204 132 22];
            app.EditField.Value = 'Titile';

            % Create EditFieldLabel
            app.EditFieldLabel = uilabel(app.Tab_4);
            app.EditFieldLabel.FontWeight = 'bold';
            app.EditFieldLabel.Position = [16 204 29 22];
            app.EditFieldLabel.Text = '标题';

            % Create EditField_8
            app.EditField_8 = uieditfield(app.Tab_4, 'text');
            app.EditField_8.FontWeight = 'bold';
            app.EditField_8.Position = [10 153 218 22];
            app.EditField_8.Value = '线条1,线条2';

            % Create Label_9
            app.Label_9 = uilabel(app.Tab_4);
            app.Label_9.FontWeight = 'bold';
            app.Label_9.Position = [8 174 109 22];
            app.Label_9.Text = '图例(英文逗号隔离)';

            % Create Label_4
            app.Label_4 = uilabel(app.Tab_4);
            app.Label_4.HorizontalAlignment = 'right';
            app.Label_4.FontWeight = 'bold';
            app.Label_4.Position = [0 107 77 22];
            app.Label_4.Text = '字体样式选取';

            % Create DropDown_2
            app.DropDown_2 = uidropdown(app.Tab_4);
            app.DropDown_2.Items = {'默认', '宋体', '新罗马', '黑体', '楷体', '简雅黑'};
            app.DropDown_2.FontWeight = 'bold';
            app.DropDown_2.Position = [92 107 135 22];
            app.DropDown_2.Value = '默认';

            % Create EditField_3
            app.EditField_3 = uieditfield(app.Tab_4, 'text');
            app.EditField_3.FontWeight = 'bold';
            app.EditField_3.Position = [134 76 94 22];
            app.EditField_3.Value = '12';

            % Create Label_3
            app.Label_3 = uilabel(app.Tab_4);
            app.Label_3.FontWeight = 'bold';
            app.Label_3.Position = [3 76 53 22];
            app.Label_3.Text = '字体大小';

            % Create EditField_6
            app.EditField_6 = uieditfield(app.Tab_4, 'text');
            app.EditField_6.FontWeight = 'bold';
            app.EditField_6.Position = [133 42 93 22];
            app.EditField_6.Value = '[1.5,1.5]';

            % Create Label_7
            app.Label_7 = uilabel(app.Tab_4);
            app.Label_7.FontWeight = 'bold';
            app.Label_7.Position = [6 42 53 22];
            app.Label_7.Text = '线条粗细';

            % Create EditField_7
            app.EditField_7 = uieditfield(app.Tab_4, 'text');
            app.EditField_7.FontWeight = 'bold';
            app.EditField_7.Position = [135 10 91 22];
            app.EditField_7.Value = '-*,-^';

            % Create Label_8
            app.Label_8 = uilabel(app.Tab_4);
            app.Label_8.FontWeight = 'bold';
            app.Label_8.Position = [5 10 133 22];
            app.Label_8.Text = '线条样式(英文逗号隔离)';

            % Create Tab_5
            app.Tab_5 = uitab(app.TabGroup2);
            app.Tab_5.Title = '细微设置';
            app.Tab_5.BackgroundColor = [1 1 1];

            % Create x010010EditField
            app.x010010EditField = uieditfield(app.Tab_5, 'text');
            app.x010010EditField.FontWeight = 'bold';
            app.x010010EditField.Position = [162 270 66 22];
            app.x010010EditField.Value = '0';

            % Create xLabel
            app.xLabel = uilabel(app.Tab_5);
            app.xLabel.FontWeight = 'bold';
            app.xLabel.Position = [5 270 158 22];
            app.xLabel.Text = 'x轴范围:若0到10,输入 [0,10]';

            % Create y1515EditField
            app.y1515EditField = uieditfield(app.Tab_5, 'text');
            app.y1515EditField.FontWeight = 'bold';
            app.y1515EditField.Position = [162 239 66 22];
            app.y1515EditField.Value = '0';

            % Create yLabel
            app.yLabel = uilabel(app.Tab_5);
            app.yLabel.FontWeight = 'bold';
            app.yLabel.Position = [5 239 148 22];
            app.yLabel.Text = 'y轴范围:若1到5 ,输入 [1,5]';

            % Create x134EditField
            app.x134EditField = uieditfield(app.Tab_5, 'text');
            app.x134EditField.FontWeight = 'bold';
            app.x134EditField.Position = [144 204 82 22];
            app.x134EditField.Value = '0';

            % Create xLabel_2
            app.xLabel_2 = uilabel(app.Tab_5);
            app.xLabel_2.FontWeight = 'bold';
            app.xLabel_2.Position = [7 204 138 22];
            app.xLabel_2.Text = 'x轴刻度位置如例 [1,3,4] ';

            % Create y12100EditField
            app.y12100EditField = uieditfield(app.Tab_5, 'text');
            app.y12100EditField.FontWeight = 'bold';
            app.y12100EditField.Position = [156 163 71 22];
            app.y12100EditField.Value = '0';

            % Create yLabel_2
            app.yLabel_2 = uilabel(app.Tab_5);
            app.yLabel_2.FontWeight = 'bold';
            app.yLabel_2.Position = [7 163 149 22];
            app.yLabel_2.Text = 'y轴刻度位置如例 [1:2:100]';

            % Create xA1A2EditField
            app.xA1A2EditField = uieditfield(app.Tab_5, 'text');
            app.xA1A2EditField.FontWeight = 'bold';
            app.xA1A2EditField.Position = [3 93 226 23];
            app.xA1A2EditField.Value = '0';

            % Create xLabel_3
            app.xLabel_3 = uilabel(app.Tab_5);
            app.xLabel_3.FontWeight = 'bold';
            app.xLabel_3.Position = [3 119 232 23];
            app.xLabel_3.Text = 'x轴刻度替换，替代原来数字，例如 A1,A2';

            % Create yEditField_2
            app.yEditField_2 = uieditfield(app.Tab_5, 'text');
            app.yEditField_2.FontWeight = 'bold';
            app.yEditField_2.Position = [5 32 222 23];
            app.yEditField_2.Value = '0';

            % Create yLabel_3
            app.yLabel_3 = uilabel(app.Tab_5);
            app.yLabel_3.FontWeight = 'bold';
            app.yLabel_3.Position = [2 52 233 23];
            app.yLabel_3.Text = 'y轴刻度替换，替代原来数字,英文逗号隔开';

            % Create Tab_6
            app.Tab_6 = uitab(app.TabGroup2);
            app.Tab_6.Title = 'Tab';

            % Create DropDown_4Label
            app.DropDown_4Label = uilabel(app.Tab);
            app.DropDown_4Label.HorizontalAlignment = 'right';
            app.DropDown_4Label.FontSize = 14;
            app.DropDown_4Label.FontWeight = 'bold';
            app.DropDown_4Label.FontColor = [0.3294 0.4588 0.1569];
            app.DropDown_4Label.Position = [446 227 61 22];
            app.DropDown_4Label.Text = '形式选择';

            % Create DropDown_4
            app.DropDown_4 = uidropdown(app.Tab);
            app.DropDown_4.Items = {'普通折线图', '阶梯图', '误差棒折线图', '误差带折线图'};
            app.DropDown_4.FontSize = 14;
            app.DropDown_4.FontWeight = 'bold';
            app.DropDown_4.FontColor = [0.3294 0.4588 0.1569];
            app.DropDown_4.Position = [526 229 132 22];
            app.DropDown_4.Value = '普通折线图';

            % Create Panel_3
            app.Panel_3 = uipanel(app.Tab);
            app.Panel_3.Title = '基础颜色设置块';
            app.Panel_3.BackgroundColor = [0.902 0.9882 0.9725];
            app.Panel_3.FontWeight = 'bold';
            app.Panel_3.FontSize = 14;
            app.Panel_3.Position = [239 122 436 103];

            % Create EditField_4
            app.EditField_4 = uieditfield(app.Panel_3, 'text');
            app.EditField_4.FontWeight = 'bold';
            app.EditField_4.Position = [117 44 91 22];
            app.EditField_4.Value = '[1,3]';

            % Create Label_5
            app.Label_5 = uilabel(app.Panel_3);
            app.Label_5.FontWeight = 'bold';
            app.Label_5.Position = [5 8 114 58];
            app.Label_5.Text = {'默认配色选取 '; '若选表格标号1,3'; '对应配色则输入[1,3]'; '若不选输入0'};

            % Create EditField_5
            app.EditField_5 = uieditfield(app.Panel_3, 'text');
            app.EditField_5.FontWeight = 'bold';
            app.EditField_5.Position = [335 44 92 22];
            app.EditField_5.Value = '[0]';

            % Create Label_6
            app.Label_6 = uilabel(app.Panel_3);
            app.Label_6.FontWeight = 'bold';
            app.Label_6.Position = [223 8 114 58];
            app.Label_6.Text = {'自取配色选取 '; '若选表格标号1,3'; '对应配色则输入[1,3]'; '若不选输入[0]'};

            % Create Panel_4
            app.Panel_4 = uipanel(app.Tab);
            app.Panel_4.Title = '数据导入块';
            app.Panel_4.BackgroundColor = [0.9137 0.9608 0.9216];
            app.Panel_4.FontWeight = 'bold';
            app.Panel_4.FontSize = 13;
            app.Panel_4.Position = [2 437 231 263];

            % Create Button_9
            app.Button_9 = uibutton(app.Panel_4, 'push');
            app.Button_9.ButtonPushedFcn = createCallbackFcn(app, @Button_9Pushed, true);
            app.Button_9.FontSize = 13;
            app.Button_9.FontWeight = 'bold';
            app.Button_9.Position = [8 206 71 26];
            app.Button_9.Text = '导入数据';

            % Create DropDown
            app.DropDown = uidropdown(app.Panel_4);
            app.DropDown.Items = {'mat数据', 'excel数据'};
            app.DropDown.ValueChangedFcn = createCallbackFcn(app, @DropDownValueChanged, true);
            app.DropDown.FontSize = 13;
            app.DropDown.FontWeight = 'bold';
            app.DropDown.Position = [104 208 104 22];
            app.DropDown.Value = 'mat数据';

            % Create x1lengthyLabel
            app.x1lengthyLabel = uilabel(app.Panel_4);
            app.x1lengthyLabel.FontWeight = 'bold';
            app.x1lengthyLabel.Position = [5 78 122 43];
            app.x1lengthyLabel.Text = {'x轴数据选取行数，若'; '第一行为x轴则填 1'; '（0默认1:length(y)）'};

            % Create xx101lengthyEditField
            app.xx101lengthyEditField = uieditfield(app.Panel_4, 'text');
            app.xx101lengthyEditField.FontWeight = 'bold';
            app.xx101lengthyEditField.Position = [126 99 101 22];
            app.xx101lengthyEditField.Value = '0';

            % Create y23y23EditField
            app.y23y23EditField = uieditfield(app.Panel_4, 'text');
            app.y23y23EditField.FontWeight = 'bold';
            app.y23y23EditField.Position = [114 38 112 22];
            app.y23y23EditField.Value = '[1,2]';

            % Create y23y23Label
            app.y23y23Label = uilabel(app.Panel_4);
            app.y23y23Label.FontWeight = 'bold';
            app.y23y23Label.Position = [8 17 108 43];
            app.y23y23Label.Text = {'y轴数据选取行数，'; '若第2,3行为y轴数'; '据则填 [2,3]'};

            % Create Label_14
            app.Label_14 = uilabel(app.Panel_4);
            app.Label_14.HorizontalAlignment = 'right';
            app.Label_14.FontSize = 13;
            app.Label_14.FontWeight = 'bold';
            app.Label_14.Position = [4 141 83 22];
            app.Label_14.Text = '数据导入形式';

            % Create DropDown_5
            app.DropDown_5 = uidropdown(app.Panel_4);
            app.DropDown_5.Items = {'指定行/列导入', '全部导入'};
            app.DropDown_5.FontSize = 13;
            app.DropDown_5.FontWeight = 'bold';
            app.DropDown_5.Position = [102 141 120 22];
            app.DropDown_5.Value = '指定行/列导入';

            % Create Label_16
            app.Label_16 = uilabel(app.Panel_4);
            app.Label_16.HorizontalAlignment = 'right';
            app.Label_16.FontSize = 13;
            app.Label_16.FontWeight = 'bold';
            app.Label_16.Position = [4 171 83 22];
            app.Label_16.Text = '数据是否转置';

            % Create DropDown_7
            app.DropDown_7 = uidropdown(app.Panel_4);
            app.DropDown_7.Items = {'不转置', '转置'};
            app.DropDown_7.FontSize = 13;
            app.DropDown_7.FontWeight = 'bold';
            app.DropDown_7.Position = [118 171 104 22];
            app.DropDown_7.Value = '不转置';

            % Create Panel
            app.Panel = uipanel(app.Tab);
            app.Panel.Title = '误差设置块';
            app.Panel.BackgroundColor = [0.8 0.8784 0.8588];
            app.Panel.FontWeight = 'bold';
            app.Panel.FontSize = 14;
            app.Panel.Position = [1 1 489 94];

            % Create EditField_9
            app.EditField_9 = uieditfield(app.Panel, 'text');
            app.EditField_9.FontWeight = 'bold';
            app.EditField_9.Position = [132 40 68 22];
            app.EditField_9.Value = '[6,7]';

            % Create EditField_9Label
            app.EditField_9Label = uilabel(app.Panel);
            app.EditField_9Label.FontWeight = 'bold';
            app.EditField_9Label.Position = [7 40 125 22];
            app.EditField_9Label.Text = '误差上限数据选取行数';

            % Create EditField_10
            app.EditField_10 = uieditfield(app.Panel, 'text');
            app.EditField_10.FontWeight = 'bold';
            app.EditField_10.Position = [132 6 68 22];
            app.EditField_10.Value = '[6,7]';

            % Create EditField_10Label
            app.EditField_10Label = uilabel(app.Panel);
            app.EditField_10Label.FontWeight = 'bold';
            app.EditField_10Label.Position = [7 6 125 22];
            app.EditField_10Label.Text = '误差下限数据选取行数';

            % Create EditField_11
            app.EditField_11 = uieditfield(app.Panel, 'text');
            app.EditField_11.Position = [445 2 35 22];
            app.EditField_11.Value = '10';

            % Create Label_21
            app.Label_21 = uilabel(app.Panel);
            app.Label_21.FontWeight = 'bold';
            app.Label_21.Position = [366 2 87 22];
            app.Label_21.Text = '误差棒大小';

            % Create EditField_13
            app.EditField_13 = uieditfield(app.Panel, 'text');
            app.EditField_13.FontWeight = 'bold';
            app.EditField_13.Position = [301 35 60 22];
            app.EditField_13.Value = '[0]';

            % Create Label_13
            app.Label_13 = uilabel(app.Panel);
            app.Label_13.FontWeight = 'bold';
            app.Label_13.Position = [213 35 89 22];
            app.Label_13.Text = '默认误差带颜色';

            % Create EditField_15
            app.EditField_15 = uieditfield(app.Panel, 'text');
            app.EditField_15.FontWeight = 'bold';
            app.EditField_15.Position = [298 4 63 22];
            app.EditField_15.Value = '[0]';

            % Create Label_18
            app.Label_18 = uilabel(app.Panel);
            app.Label_18.FontWeight = 'bold';
            app.Label_18.Position = [210 4 89 22];
            app.Label_18.Text = '自取误差带颜色';

            % Create EditField_16
            app.EditField_16 = uieditfield(app.Panel, 'text');
            app.EditField_16.Position = [445 35 35 22];
            app.EditField_16.Value = '6';

            % Create Label_22
            app.Label_22 = uilabel(app.Panel);
            app.Label_22.FontWeight = 'bold';
            app.Label_22.Position = [366 35 87 22];
            app.Label_22.Text = '图标记大小';

            % Create DropDown_8
            app.DropDown_8 = uidropdown(app.Tab);
            app.DropDown_8.Items = {'开', '半开', '关'};
            app.DropDown_8.FontSize = 13;
            app.DropDown_8.FontWeight = 'bold';
            app.DropDown_8.Position = [582 38 84 22];
            app.DropDown_8.Value = '开';

            % Create DropDown_9Label
            app.DropDown_9Label = uilabel(app.Tab);
            app.DropDown_9Label.HorizontalAlignment = 'right';
            app.DropDown_9Label.FontSize = 13;
            app.DropDown_9Label.FontWeight = 'bold';
            app.DropDown_9Label.Position = [494 67 57 22];
            app.DropDown_9Label.Text = '图框选择';

            % Create DropDown_9
            app.DropDown_9 = uidropdown(app.Tab);
            app.DropDown_9.Items = {'全框', '半框'};
            app.DropDown_9.FontSize = 13;
            app.DropDown_9.FontWeight = 'bold';
            app.DropDown_9.Position = [582 67 84 22];
            app.DropDown_9.Value = '全框';

            % Create Label_19
            app.Label_19 = uilabel(app.Tab);
            app.Label_19.HorizontalAlignment = 'right';
            app.Label_19.FontSize = 13;
            app.Label_19.FontWeight = 'bold';
            app.Label_19.Position = [494 38 71 22];
            app.Label_19.Text = '图网格选择';

            % Create Label_20
            app.Label_20 = uilabel(app.Tab);
            app.Label_20.HorizontalAlignment = 'right';
            app.Label_20.FontSize = 13;
            app.Label_20.FontWeight = 'bold';
            app.Label_20.Position = [494 7 71 22];
            app.Label_20.Text = '图例框选择';

            % Create DropDown_10
            app.DropDown_10 = uidropdown(app.Tab);
            app.DropDown_10.Items = {'有框', '无框'};
            app.DropDown_10.FontSize = 13;
            app.DropDown_10.FontWeight = 'bold';
            app.DropDown_10.Position = [582 7 84 22];
            app.DropDown_10.Value = '有框';

            % Create DropDown_11Label
            app.DropDown_11Label = uilabel(app.Tab);
            app.DropDown_11Label.HorizontalAlignment = 'right';
            app.DropDown_11Label.FontSize = 13;
            app.DropDown_11Label.FontWeight = 'bold';
            app.DropDown_11Label.Position = [239 228 57 22];
            app.DropDown_11Label.Text = '美化样式';

            % Create DropDown_11
            app.DropDown_11 = uidropdown(app.Tab);
            app.DropDown_11.Items = {'美化样式 1', '美化样式 2', '美化样式 3', '美化样式 4', '美化样式 5', '美化样式 6'};
            app.DropDown_11.FontSize = 13;
            app.DropDown_11.FontWeight = 'bold';
            app.DropDown_11.Position = [311 228 100 22];
            app.DropDown_11.Value = '美化样式 1';

            % Create EditField_17
            app.EditField_17 = uieditfield(app.Tab, 'text');
            app.EditField_17.FontSize = 13;
            app.EditField_17.FontWeight = 'bold';
            app.EditField_17.Position = [589 96 68 22];
            app.EditField_17.Value = '1.5';

            % Create EditField_17Label
            app.EditField_17Label = uilabel(app.Tab);
            app.EditField_17Label.FontSize = 13;
            app.EditField_17Label.FontWeight = 'bold';
            app.EditField_17Label.Position = [503 96 57 22];
            app.EditField_17Label.Text = '图框粗细';

            % Create Button
            app.Button = uibutton(app.UIFigure, 'push');
            app.Button.ButtonPushedFcn = createCallbackFcn(app, @ButtonPushed, true);
            app.Button.BackgroundColor = [0.3569 0.5412 0.4039];
            app.Button.FontSize = 14;
            app.Button.FontWeight = 'bold';
            app.Button.FontColor = [1 1 1];
            app.Button.Position = [819 675 84 40];
            app.Button.Text = '自取配色';

            % Create UITable
            app.UITable = uitable(app.UIFigure);
            app.UITable.ColumnName = {'label'; 'color'};
            app.UITable.ColumnWidth = {30, 50};
            app.UITable.RowName = {};
            app.UITable.Position = [684 203 105 454];

            % Create UITable_2
            app.UITable_2 = uitable(app.UIFigure);
            app.UITable_2.BackgroundColor = [1 1 1;0.9412 0.9412 0.9412;1 1 1];
            app.UITable_2.ColumnName = {'label'; 'color'};
            app.UITable_2.ColumnWidth = {30, 50};
            app.UITable_2.RowName = {};
            app.UITable_2.Position = [809 203 104 454];

            % Create Button_2
            app.Button_2 = uibutton(app.UIFigure, 'push');
            app.Button_2.ButtonPushedFcn = createCallbackFcn(app, @Button_2Pushed, true);
            app.Button_2.BackgroundColor = [0.8 0.8 0.8];
            app.Button_2.FontSize = 14;
            app.Button_2.FontWeight = 'bold';
            app.Button_2.FontColor = [0.149 0.149 0.149];
            app.Button_2.Position = [697 675 84 40];
            app.Button_2.Text = '默认配色';

            % Create Panel_2
            app.Panel_2 = uipanel(app.UIFigure);
            app.Panel_2.Title = '图片导出块';
            app.Panel_2.BackgroundColor = [1 1 1];
            app.Panel_2.FontWeight = 'bold';
            app.Panel_2.FontSize = 14;
            app.Panel_2.Position = [697 9 216 166];

            % Create Button_7
            app.Button_7 = uibutton(app.Panel_2, 'push');
            app.Button_7.ButtonPushedFcn = createCallbackFcn(app, @Button_7Pushed, true);
            app.Button_7.FontSize = 14;
            app.Button_7.FontWeight = 'bold';
            app.Button_7.Position = [7 106 100 26];
            app.Button_7.Text = '导出图片';

            % Create Button_8
            app.Button_8 = uibutton(app.Panel_2, 'push');
            app.Button_8.ButtonPushedFcn = createCallbackFcn(app, @Button_8Pushed, true);
            app.Button_8.FontSize = 14;
            app.Button_8.FontWeight = 'bold';
            app.Button_8.Position = [117 106 100 26];
            app.Button_8.Text = '放大镜';

            % Create cm8cm128EditField
            app.cm8cm128EditField = uieditfield(app.Panel_2, 'text');
            app.cm8cm128EditField.FontWeight = 'bold';
            app.cm8cm128EditField.Position = [126 63 64 31];
            app.cm8cm128EditField.Value = '[12,8]';

            % Create cm8cm128EditFieldLabel
            app.cm8cm128EditFieldLabel = uilabel(app.Panel_2);
            app.cm8cm128EditFieldLabel.FontWeight = 'bold';
            app.cm8cm128EditFieldLabel.Position = [19 51 96 43];
            app.cm8cm128EditFieldLabel.Text = {'导出图片大小，'; '若长12cm宽8cm'; ',则可输入[12,8]'};

            % Create Label_11
            app.Label_11 = uilabel(app.Panel_2);
            app.Label_11.HorizontalAlignment = 'right';
            app.Label_11.FontWeight = 'bold';
            app.Label_11.Position = [19 3 53 29];
            app.Label_11.Text = {'图片导出'; '单位选取'};

            % Create DropDown_3
            app.DropDown_3 = uidropdown(app.Panel_2);
            app.DropDown_3.Items = {'centimeters', 'pixels', 'normalized', 'inches', 'points', 'characters'};
            app.DropDown_3.FontWeight = 'bold';
            app.DropDown_3.Position = [87 10 100 22];
            app.DropDown_3.Value = 'centimeters';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = picture_plot

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end