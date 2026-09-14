实验 算法python线性回归实验
【实验名称】
Python线性回归实验
【实验要求】
掌握Python线性回归模型应用过程，根据模型要求进行数据预处理，建模，评价与应用；
【背景描述】
线性回归是利用数理统计中回归分析，来确定两种或两种以上变量间相互依赖的定量关系的一种统计分析方法，运用十分广泛。其表达形式为y = w'x+e，e为误差服从均值为0的正态分布。
【知识准备】
了解线性回归模型的使用场景，数据标准。了解Python/Spark数据处理一般方法。了解spark模型调用，训练以及应用方法
【实验设备】
Windows或Linux操作系统的计算机。部署Python，本实验提供centos6.8环境。
【实验说明】
采用成绩数据集作为算法数据，对模型进行训练和回归。
【实验环境】
Pyrhon3.X，实验在命令行python中进行，或者把代码写在py脚本，由于本次为实验，以学习模型为主，所以在命令行中逐步执行代码，以便更加清晰地了解整个建模流程。
【实验步骤】
第一步：启动python：
命令行键入python,启动python终端
第二步：导入用到的包，并读取数据：
(1).导入包:
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import scipy
(2).读取数据并随机打乱,文件路径为:/opt/algorithm/scoreset/scoregather.txt
df=pd.read_csv("/opt/algorithm/scoreset/scoregather.txt",index_col=0,header=0).sample(frac=1)
(3).展示数据
df.head()

第三步：数据预处理
说明,数据集包含25门已修学科,以及一门目标学科
(1).划分训练集,测试集
PP = 0.8
df_train = df.iloc[:int(np.ceil(len(df) * PP))]
df_test = df.iloc[int(np.ceil(len(df) * PP)):]
(2).数据标准化,获取每列均值,标准差
avg_col = df_train.mean()
td_col = df_train.std()
(3).标准化结果
df_train_norm = (df_train - avg_col) / td_col
df_train_norm.head()

第四步：特征提取及线性回归模型训练
基于F检验的特征选择
(1).由于建模需要标准化字符串,故需重命名表头
list_columns_to_train = df_train_norm.columns
change_columns = ['A' + str(zr + 1) for zr in np.arange(len(list_columns_to_train))]
df_train_nor⹭潣畬湭⁳‽档湡敧损汯浵獮挍⁯‽楤瑣稨灩挨慨杮彥潣畬湭ⱳ氠獩彴潣畬湭彳潴瑟慲湩⤩損晥删瑟慲獮潦浲搨瑡㵡嵛‬㵫⤰ഺ彲⁌‽慤慴歛孝嵫猍慨数㴠渠⹰慭⡴慤慴⸩桳灡൥归⁴‽灮種牥獯猨慨数ഩ潦⁲⁩湩渠⹰牡湡敧猨慨数せ⥝ഺ††潦⁲⁪湩渠⹰牡湡敧猨慨数ㅛ⥝ഺ††††晩⠠⁩㴽欠 …樨℠‽⥫ഺ††††††归孴嵩橛⁝‽慤慴歛孝嵪⼠爠䱟‍†††攠楬⁦椨℠‽⥫☠⠠⁪㴽欠㨩‍†††††删瑟楛孝嵪㴠ⴠ‱‪慤慴楛孝嵫⼠爠䱟‍†††攠楬⁦椨㴠‽⥫☠⠠⁪㴽欠㨩‍†††††删瑟楛孝嵪㴠ㄠ〮⼠爠䱟‍†††攠楬⁦椨℠‽⥫☠⠠⁪㴡欠㨩‍†††††删瑟[i][j] = data[i][j] - data[i][k] * data[k][j] / r_L
return R_t
def forward_step(data, response="", F_in=0.01, F_out=0.5):
remaining = list(data.columns)
last_drop = ""
Vld = "mark"
n = len(data)
# 因变量选择列
selected = []
l = len(selected)
# 计算相关系数矩阵
corr_R = data.corr()
mark = 1
while (mark):
    # 首次变量选择
    if l != (len(data.columns) - 1):
        r_taget = pd.Series(np.diagonal(np.mat(corr_R)))
        r_taget.index = remaining
        Vi = corr_R[response] ** 2 / r_taget
        Vc = Vi.drop(selected + [re灳湯敳ⱝ愠楸㵳⤰献牯彴慶畬獥⤨ⵛ崱‍†††嘠⁬‽楖搮潲⡰敳敬瑣摥⬠嬠敲灳湯敳ⱝ愠楸㵳⤰献牯彴慶畬獥⤨椮摮硥ⵛ崱‍†††椠⁦汖⁤㴽氠獡彴牤灯ഺ††††††慭歲㴠〠‍†††攠楬⁦汖⁤㴡氠獡彴牤灯ഺ††††††楆㴠嘠⁣‪渨ⴠ氠ⴠ㈠  爨瑟条瑥牛獥潰獮嵥ⴠ嘠⥣‍†††††䘠瑟獥⁴‽捳灩⹹瑳瑡⹳⹦獩⡦彆湩‬ⰱ⠠⁮‭⁬‭⤲ഩ††††††晩䘠⁩‾彆整瑳ഺ††††††††敳敬瑣摥愮灰湥⡤汖ഩ††††††††⁬‽敬⡮敳敬瑣摥ഩ                # 协方差矩阵转换
                corr_R = pd.DataFrame(R_transform(np.array(corr_R), remaining.index(Vl)))
                corr_R.index = data.columns
                corr_R.columns = data.columns
                if l >= 2:  # 考虑剔除变量
             †††映牯椠椠⁮灮愮慲杮⡥敬⡮敳敬瑣摥⤩ഺ††††††††††††摲瑟条瑥㴠瀠⹤敓楲獥渨⹰楤条湯污渨⹰慭⡴潣牲剟⤩ഩ††††††††††††摲瑟条瑥椮摮硥㴠爠浥楡楮杮‍†††††††††††嘠摩㴠挠牯彲孒敲灳湯敳⁝⨪㈠⼠爠彤慴敧൴††††††††††††捖⁤‽楖孤敳敬瑣摥⹝潳瑲癟污敵⡳獡散摮湩㵧慆獬⥥ⵛ崱‍†††††††††††嘠摬㴠嘠摩獛汥捥整嵤献牯彴慶畬獥愨捳湥楤杮䘽污敳⸩湩敤學ㄭ൝††††††††††††摆㴠嘠摣⨠⠠⁮‭氨ⴠㄠ ‭⤲⼠爠彤慴敧孴敲灳湯敳൝ࠀࠢࠤࠦ࠮࠲࠴࠶ࡌࡎࡐࡘ࡜࡞ࡢࡤࢲࢴࢶࢾࣂࣄॶॸॺং঄আਂ਄ਆ਎਒ਔ싗귗誜흸흣読誜흸ퟂ読흸ퟂ読흸ퟂ­ᔩၨ屲ᘀꉨ䘣㔀脈䩃䩏䩐䩑࡜憁ᕊ漀Ĩᔣၨ屲ᘀၨ屲䌀ᭊ伀͊倀͊儀͊愀ᕊ漀Ĩᔣၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊愀ᕊ漀Ĩᔠၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊愀ᕊᔩၨ屲ᘀၨ屲㔀脈䩃䩏䩐䩑࡜憁ᕊ漀Ĩᔩၨ屲ᘀ繨᰺㔀脈䩃䩏䩐䩑࡜憁ᕊ漀Ĩᔦၨ屲ᘀ繨᰺㔀脈䩃䩏䩐䩑࡜憁ᕊᔓၨ屲ᘀၨ屲愀ᕊ漀Ĩᔓၨ屲ᘀ繨᰺愀ᕊ漀Ĩ℀ࠀࠤ࠴ࡎ࡞ࢴࣄॸআ਄ਔ੶઄઺ૈ୲஀ஜொ௮ంన౐ಜಶമ෪෼úêêêêêêêêêêêêêༀ萑Ȝ搒ĠꐔǴ䑗È葠Ȝ摧爐\Ѐ摧爐\ᬀਔਢ੒੘੨ੲੴ੶੸઀ં઄શસ઺઼ૄ૆ૈ୰୲୴���럋랢箍쭪ꊷ趷奻Cᔫၨ屲ᘀ繨᰺㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈桰ᔠၨ屲ᘀၨ屲䌀ᭊ伀͊倀͊儀͊愀ᕊᔠၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊愀ᕊᔣၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊愀ᕊ漀Ĩᔩၨ屲ᘀၨ屲㔀脈䩃䩏䩐䩑࡜憁ᕊ漀Ĩᔩၨ屲ᘀ繨᰺㔀脈䩃䩏䩐䩑࡜憁ᕊ漀Ĩᔦၨ屲ᘀ繨᰺㔀脈䩃䩏䩐䩑࡜憁ᕊᔣၨ屲ᘀၨ屲䌀ᭊ伀͊倀͊儀͊愀ᕊ漀Ĩᔣၨ屲ᘀ彨퐼䌀ᭊ伀͊倀͊儀͊愀ᕊ漀Ĩᔠၨ屲ᘀ彨퐼䌀ᭊ伀͊倀͊儀͊愀ᕊᔀ୴୼୾஀சஜைொ௬௮ఀందన౎౐ಚಜ಴ಶೞബമ෨෪෺෼ฎฐ틨辺轺轺轺ꓒ窏뫨撏ᔫၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜澁Ĩ桰ᔨၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜炁hᔨၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜炁hᔫၨ屲ᘀၨ屲㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈桰ᔮၨ屲ᘀၨ屲㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈⡯瀁hᔫၨ屲ᘀ繨᰺㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈桰ᔮၨ屲ᘀ繨᰺㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈⡯瀁hᰀ෼ฐดศ๚๶ຈ໨ཆ཰ྤ࿔࿨၄ၮၲၶႚႰტᄾᇨማቑተኁኜኲïïïïïïïïïïïïïïༀ萑Ȝ搒ĠꐔǴ䑗È葠Ȝ摧爐\ᬀฐฒดฦศ๘๚๴๶ຆຈ໦໨ངཆ཮཰ྡྷྤ࿒࿔࿦࿨၂၄ၬၮ쳤鲴鲴鲴犇犇犇鲴犇犇鲴犇岇ᔫၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜澁Ĩ桰ᔨၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜炁hᔨၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜炁hᔮၨ屲ᘀၨ屲㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈⡯瀁hᔮၨ屲ᘀ繨᰺㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈⡯瀁hᔯၨ屲ᘀၨ屲䌀ᭊ伀͊倀͊儀͊洀H渄H漄Ĩ䡳Ѐ䡴Ѐ̵jᔀၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊唀Ĉ䡭Ѐ䡮Ѐ䡳Ѐ䡴Ѐᨀၮၰၲၴၶ႘ႚႮႰრტᄼᄾᇦᇨሚማቐ퇤麶檄檄檄㱓㱓㱓Sᔬၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀hᔬၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀hᔲၨ屲ᘀၨ屲㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈䩡⡯瀁hᔲၨ屲ᘀ繨᰺㔀脈⩂䌁ᭊ伀͊倀͊儀͊尀脈䩡⡯瀁hᔯၨ屲ᘀၨ屲䌀ᭊ伀͊倀͊儀͊洀H渄H漄Ĩ䡳Ѐ䡴Ѐ̵ﵪᔀၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊唀Ĉ䡭Ѐ䡮Ѐ䡳Ѐ䡴Ѐᔥၨ屲ᘀၨ屲㔀脈䩃䩏䩐䩑࡜澁Ĩ̵䭪_ᔀၨ屲ᘀ繨᰺䌀ᭊ伀͊倀͊儀͊唀Ĉ䡭Ѐ䡮Ѐ䡳Ѐ䡴Ѐᄀቐቑቯተኀኁኛኜ኱ኲዏዐዱዲ጑ጒጺጻ፜፝ᎊᎋᎬᎭᏎᏏᏰᏱᑦᑨᑼᑾᓲᓴᔰᔲᕎᕐᕨᕪᖄᖆᖖᖘᖲᖴᗖᗘᗬᗮᘖᘘᘨᘪᙄᙆᙞᙠᚨᚪ᜚᜜᝞ᝠ탧킹킹킹킹킹킹킹킹킹킹킹킹킹킹탧킹킹킹킹ꆹ탧킹ꆹ탧킹킹ꆹ탧킹킹¹ᔯၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜憁ᕊ漀Ĩ桰ᔬၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀hᔬၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀hᔯၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜憁ᕊ漀Ĩ桰㼀ኲዐዲጒጻ፝ᎋᎭᏏᏱᑨᑾᓴᔲᕐᕪᖆᖘᖴᗘᗮᘘᘪᙆᙠᚪ᜜ᝠïïïïïïïïïïïïïïༀ萑Ȝ搒ĠꐔǴ䑗È葠Ȝ摧爐\ᬀᝠីឺᠢᠣᡮᡯᢋᢌᢠᢡᢿᣀ᣼᣽᤹᤺ᥕᥖ᥹᥺ᦛᨀᨲᨴ᫦᫨ᬾᭀᮚᮜᯤ᯦ᰩᰪᱳᱴᲦᲧ᳥᳦ᴲᴳᶅᶆ᷐᷏㐀㒦㒨㔂㔄㕤㕦㖼㖾㚊㚌㛺㛼㝮㝰㟊㟌틩틩틩틩틩틩틩틩틩틩틩ꊺ틩틩틩ꊺ틩틩틩틩틩틩틩Ò唃Ĉᔯၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜憁ᕊ漀Ĩ桰ᔯၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜憁ᕊ漀Ĩ桰ᔬၨ屲ᘀၨ屲䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀hᔬၨ屲ᘀ繨᰺䈀Ī䩃䩏䩐䩑࡜憁ᕊ瀀h㼀ᝠឺᠣᡯᢌᢡᣀ᣽᤺ᥖ᥺ᦜᨴ᫨ᭀᮜ᯦ᰪᱴᲧ᳦ᴳᶆ᷐㒨㔄㕦㖾ïïïïïïïïïïïïïïༀ萑Ȝ搒ĠꐔǴ䑗È葠Ȝ摧爐\ᬀ                        F_test_out = scipy.stats.f.isf(F_out, 1, (n - (l - 1) - 2))
                        if (Fd < F_test_out):
                            selected.remove(Vld)
                            last_drop = Vld
                            corr_R = pd.DataFrame(R_transform(np.array(corr_R), remaining.index(Vld)))
                            corr_R.index = data.columns
                            corr_R.columns = data.columns
                            l = len(selected)
            else:
                mark = 0
    else:
        mark = 0
return selected
select_list = forward_step(df_train_norm, response=change_columns[-1])
select_list = change_columns[:2]
# 线性回归模型训练
formula = "{} ~ {} + 1".format(change_columns[-1], ' + '.join(select_list))
model = smf.ols(formula, df_train_norm).fit()
print(model.summary())

第五步：模型预测展示与结果对比
# 模型预测展示
# 利用训练集的统计信息标准化测试数据
df_test_norm = (df_test - avg_col) / td_col
df_test_norm.columns = change_columns
df_test_norm.head

#模型预测展示
#利用训练集的统计信息标准化测试数据
df_test_norm = (df_test - avg_col) / td_col
df_test_norm.columns = change_columns
#预测结果还原百分制
predict = model.predict(df_test_norm)
predict_df = predict * td_col[-1] + avg_col[-1]
#被选择特征反编码
select_list_old = [co[z] for z in select_list]
print(predict_df)

print(select_list_old[0]);print(select_list_old[1])

#结果对比
F = pd.DataFrame(df_test["目标学科"]).join(pd.DataFrame(predict_df))
#回归残差,以及结果相关系数
corr = F.corr()["目标学科"][0]
stds = abs(F["目标学科"] - F[0]).sum() / len(F)
# 输出程序运行摘要
print("程序选择特征 %s,预测结果相关系数 is %s,回归残差 is %s 分" % (",".join(select_list_old), corr, stds))

第六步:通过以下命令执行python文件,直接查看运行结果
python /opt/algorithm/scoreset/scorexpect.py

【问题与回答】
1、Q：为什么要进行标准化，而且必须用正规化方法？
A：线性回归基本假设之一，所有变量必须满足正态分布假设，但在实际操作上，我们一般利用正规化方法让数据近似于正态分布。在某些情况下，数据实在是呈现出严重的偏态特征，可以选用boxcox方法转换数据，尽量达到线型回归模型的数据要求。
2、Q：怎么防止线性回归过拟合？
A：模型过拟合是一个普遍性问题，尤其在特征非常多而样本量却很少的情况下，在实践中，一般通过特征降维以及增加正则化参数的方式共同使用，防止模型过拟合，对于特征过多而且普遍独立的情况下，采用本例的基于F检验特征筛选方法提取变量效果较好，一般的降维方法有主成分分析法，主基底映射法，另外，在模型构建阶段，有向前法，后退法，以及逐步回归法，本例的检验特征提取方法类似于逐步回归法。数据降维在提高模型精度方面也有贡献，由于某些变量之间存在共线性，会导致模型精度下降，降维是处理共线性的一个有效方法。在训练上，添加正则化方法，一般用L2范数正则化，使得某些系数值不能过大，提高模型泛化性能。

三盟科技股份有限公司
