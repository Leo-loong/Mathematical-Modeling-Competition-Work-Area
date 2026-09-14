一部分

%---------------
% initializations
%---------------
n=length(x);       %%

m=length(measvec); %%

xrecon=zeros(1,n); % max likelihood  %% xreconstruction

mrecon=zeros(1,n); % average         %%

srecon=zeros(1,n); % std_dev         %% srecon°´

pd彦彎潴䵟稽牥獯渨‬Ⱳ洠摯汥潟摲牥㬩†┠‥丠琠⁯⁍Ⱐഠ瀍晤䵟瑟彯㵎敺潲⡳Ɑ氠‬潭敤彬牯敤⥲※†┥†⁍潴丠ഠ砍㵸㨱潭敤彬牯敤㭲†硸砽⵸洨摯汥潟摲牥ㄫ⼩㬲†硸砽⽸慭⡸硸㬩†┥†഍硸砽⩸潢湵硤※‥慶畬獥漠敶⁲桷捩⁨摰⁦獩猠浡汰摥†┥ഠ瀍晤硟㵸硸഻損汥慴砽⡸⤲砭⡸⤱※┠‥ഠ
其中，xx是抽样的序列符号，即：抽多少个样、抽样间隔是由xx决定的。

二部分
%---------------
% compute signal node prior
%---------------
pdf_prior= (k/n)*normpdf(xx,0,sig_1);  %%
if (sig_0 > epsilon)                  %%  epsilon
  pdf_prior= pdf_prior  +    (1-k/n)*normpdf(xx,0,sig_0)഻汥敳‍椠㉮昽湩⡤扡⡳硸㰩灥楳潬⥮※††††††††┥ഠ†摰彦牰潩⡲湩⤲瀽晤灟楲牯椨㉮ ‫ㄨ欭港㬩†┠‥攍摮瀍晤灟楲牯瀽晤灟楲牯猯浵瀨晤灟楲牯㬩†┥†礍湟楯敳渽牯灭晤砨ⱸⰰ楳浧彡⥚※┠渠楯敳瀠楲牯礍湟楯敳礽湟楯敳猯浵礨湟楯敳㬩†┥渠楯敳ഠ摰彦牰潩㵲晩瑦桳晩⡴摰彦牰潩⥲※†┥†瀍晤硟㵸晩瑦桳晩⡴摰彦硸㬩††††┠‥ഠ硸椽晦獴楨瑦砨⥸഻役潮獩㵥晩瑦桳晩⡴役潮獩⥥഻摰㵦敺潲⡳Ɱ敬杮桴砨⥸㬩഍其中，pdf_prior是计算先验的节点概率分布值。
若有小系数，则pdf_prior= EMBED Equation.DSMT4  + EMBED Equation.DSMT4  .
若无小系数，则pdf-prior= EMBED Equation.DSMT4  + EMBED Equation.DSMT4  ，即强制初始化一些大系数。

此时，对此事得到的概率密度函数抽出xx个抽样。记为：pdf_prior。
然后归一化pdf_prior：pdf_prior=pdf_prior/sum(pdf_prior)。

关于noise的这两步没明白。
y_noise=normpdf(xx,0,sigma_Z);  % noise prior
y_noise=y_noise/sum(y_noise);  %% noise ¹éÒ»»¯

三部分

下面的这几步是进行傅里叶逆变换：
pdf_prior=ifftshift(pdf_prior);   %%
pdf_xx=ifftshift(pdf_xx);         %%
xx=ifftshift(xx);
y_noise=ifftshift(y_noise);
pdf=zeros(n,length(xx));

公式不用写了吧，就是傅里叶逆变换的公式。
这里的pdf被初始化为行数为n，列数与xx的个数相同的的矩阵。

四部分

下面正式开始BP迭代，iter为初始化的迭代次数
%---------------
% BP ITERATIONS
%---------------
for it=1:iter

迭代开始：从测量到信号开始
    %---------------
   % FORWARD ITE䅒䥔乏ⴠ映潲⁭敭獡牵浥湥獴琠⁯楳湧污‍†┠ⴭⴭⴭⴭⴭⴭⴭഭ†映牯椠ㄽ渺†┠‥ഠ†††晩⠠瑩㴽⤱┠椠楮楴污瀠晤††┠‥‍††††潦⁲牲ㄽ爺‍†††††瀠晤也瑟彯⡍Ⱪ爠Ⱳ㨠㴩摰彦牰潩⡲⤺※┠‥ഠ††††攠摮‍††攠獬⁥††††††††††††┥†‍††††敮杩扨牯㵳畡⡸ⰺ⥩㬧†††┥†‍††††敮杩扨牯㵳敳摴晩彦桳楲渨楥桧潢獲〬㬩†┥†‍††††湬氽湥瑧⡨敮杩扨牯⥳※††┠‥ഠ††††猠汥彦湩敤㵸敳晬楟摮硥⡎Ⱪ⤺※┠‥഍第一次迭代的时候先对每一个变量节点赋初值，即抽样的pdf_prior。不明白的地方：pdf_prior中的元素个数为xx，与变量节点的个数N的关系如何？
也就是文章公式中的     EMBED Equation.DSMT4  =pdf_prior

下面这几步是编程处理，等价于公式中的 EMBED Equation.DSMT4  ，即找到与该变量节点相连的测量节点，不对应具体的公式。
         neighbors=aux(:,i)';      %%  aux
         neighbors=setdiff_shri(neighbors,0);
         ln=length(neighbors);      %%
         self_index=self_indexN(i,:);  %%

五部分

下面这几步对应于由测量节点向变量节点传值，并应用MMSE方法估计变量节点的值。若为第一次迭代，则直接跳出此部分，直接进入下一个循环BACKWARD ITERATION - from signal to measurements。若不是第一次迭代，则进入本循环。

         %---------------
         % ESTIMATE SIGNAL COEFF x(i)
         %---------------
         pdf_res=[];
         for jj=1:ln    %%
            pdf_tmp=reshape(pdf_M_to_N(neighbors(jj),self_index(jj),:),1, model_order); %%
            pdf_浴㵰摰彦浴⭰灥楳潬㭮‍†††††椠⁦氨湥瑧⡨摰彦敲⥳㴽⤰┠映物瑳琠浩⁥ഠ†††††††瀠晤牟獥⠽摰彦浴⥰഻††††††汥敳┠挠湯潶畬楴湯猠整൰†††††††瀠晤牟獥洽汵摰⡦摰彦敲ⱳ摰彦浴⥰※┥ഠ††††††湥൤††††攠摮‍††††摰彦敲㵳畭灬晤瀨晤牟獥‬摰彦牰潩⥲※†┥ഠ††††椠⁦椨㹴⤱┠搠浡楰杮‍†††††瀠晤牟獥朽敭湡瀨晤牟獥瀬晤椨㨬Ⱙ慧浭彡摰灢〬㬩┠慧浭彡摰灢〽›牴敵䈠⁐┠‥‍††††湥൤††††嬠瑭ⱴ猠瑴‬慭瑸嵴洽慥癮牡慭灸晤⠨摰彦敲⥳‬硸㬩┠挠浯異整⁳瑳瑡獩楴獣‍††††牸捥湯椨㴩慭瑸㭴┠洠硡 likelihood
         mrecon(i)=mtt; % mean
         srecon(i)=stt; % std_dev around mean
         pdf(i,:)=pdf_res; % store result
其实，此部分就对应于公式（5）。
值得注意的是函数meanvarmaxpdf，如何进行MMSE估计的。Meanvarmaxpdf函数的公式如下（所用的变量表达式全部与meanvarmaxpdf.m中一致）：
1、归一化pdf：pdf=pdf/sum(pdf);
2、计算pdf中最大值mm和其所在位置ind。
3、求期望m=xx.*pdf. (因为xx为横轴上的值，pdf为其对应的概率，所以乘积是期望)
4、求xx^2的期望e2=（xx.*xx.*pdf）
5、求方差v2=e2-m*m（即对应公式 EMBED Equation.DSMT4  ）
6、求标准差sig= EMBED Equation.DSMT4
以上所求的各个变量均用来估计xx和判断迭代终止条件。

六部分

؀ࠈࠊࠪࠬࡎࡐࡰࡲ࢘࢜࢞ࢠࣆ࣐ࣶ࣌࣎ीूॄ४ঔখঘা৸৺ৼਥਲ਼਴ਵੜ੧੨੩દપફબ઺ૡૢૣ૭૮쿥꾻ꂻ꾻뮌皯뮌皯뮌皯뮌皯뮌皯뮌皯뮌皯뮌皯뮌皯꾌ᘪ୨⌅䈀Ī䩃䡋䩏䩑䩞䩡⡯瀁hᘧ牨搳䈀Ī䩃䡋䩏䩑䩞䩡桰ᔜ퉨⼬ᘀ牨搳䌀ᡊ䬀H伀ъ儀ъᘖ牨搳䌀ᡊ䬀H伀ъ儀ъᘧ牨搳䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘪ큨䡝䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᔳ큨䡝ᘀ큨䡝㔀脈⩂䌆ⱊ䬀H伀͊儀͊帀ъ愀ⱊ漀Ĩ桰ÿ⸀؀ࠈࠊࠬࡐࡲ࢞ࢠ࣐࣎ूॄখঘ৺ৼ਴ਵ੨੩ફબૢૣ૮૯ଈóçççççççççççç̀$␷㠀$⑈愀$摧㍲d̀Ĥ␷㠀$⑈愀Ĥ摧巐Hᨀ؀書ýЄĀā૮૯ଃଇଈఀెొ౎ౖ౶౸ಮರ೐೒ഠനപമ൶ඎඐกขฆง훪뛂Ʇ鶢瞋睫睫坫歷坃歷歗歃ᘧ難딭䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘧ難딭䈀Ī䩃䡋䩏䩑䩞䩡桰ᘖ難딭䌀ᡊ䬀H伀ъ儀ъᘧ難딭䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᔣ뙨堨ᘀ뙨堨㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘉ뙨堨漀Ĩᘉ難딭漀Ĩᔒ荨䉦ᘀ難딭㔀脈⡯ᘉ靨褻漀Ĩᘖ牨搳䌀ᡊ䬀H伀ъ儀ъᘧ牨搳䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘧ牨搳䈀Ī䩃䡋䩏䩑䩞䩡桰ᘪ୨⌅䈀Ī䩃䡋䩏䩑䩞䩡⡯瀁hᨀଈଉెైొౌ౎ౖ౸ರ೒പඐขงุ๩๭ທ໅໮༕༼ཎཪ྄ྃံýﴀýﴀýﴀõéééééééééﴀý̀$␷㠀$⑈愀$摧ⷺµ܀␃愁Ĥ摧⢶XĀᬀงิืุ๥๨๩๬๭ຒຖທືໄ໅໤໭໮༐༔༕༷༻༼ཌྷཎཀྵཪྂྃကဨူံퟫ쯗쮷ퟫ鳋溁ퟫ쯗ퟫ構啟_ᔒ荨䉦ᘀၨд㔀脈⡯ᔒ荨䉦ᘀ遨搽㔀脈⡯ᘉ難딭漀Ĩᔤ難딭ᘀ難딭䌀ᡊ䬀H伀ъ儀ъ洀၈猄၈ᔵ難딭ᘀ難딭䈀ପ䩃䡋䩏䩑䩞䩡䡭А桰謢"䡳Аᔵ難딭ᘀ難딭䈀Ī䩃䡋䩏䩑䩞䩡䡭А桰䡳Аᘧ難딭䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘖ難딭䌀ᡊ䬀H伀ъ儀ъᘧ難딭䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘧ難딭䈀Ī䩃䡋䩏䩑䩞䩡桰℀ံၘၚၜႆႈႊႌႎ႐႒ჀჂჄ჆წხჰᄚᄜᄞᄠᄢᄤᄦᅔᅖᅘᅚᅴᅶ쫡ꓡ쫡濡ᔒ荨䉦ᘀ睕㔀脈⡯̜ᑪ
ᔀ荨䉦ᘀ慨え㔀脈䡅￨ࡕ̭潪�੎Ĉ栕暃B栖䡡0࠵䎁ᑊ䬀H唀Ĉࡖ愁ᑊ漀Ĩ̜왪ᔀ荨䉦ᘀ慨え㔀脈䡅￠ࡕ̜乪ᔀ荨䉦ᘀ慨え㔀脈䡅￠ࡕ̭푪�੎Ĉ栕暃B栖䡡0࠵䎁ᑊ䬀H唀Ĉࡖ愁ᑊ漀Ĩ̜jᔀ荨䉦ᘀ慨え㔀脈䡅￠ࡕ̭୪�੎Ĉ栕暃B栖䡡0࠵䎁ᑊ䬀H唀Ĉࡖ愁ᑊ漀Ĩᔏ荨䉦ᘀ慨え㔀脈̘jᔀ荨䉦ᘀ慨え㔀脈ࡕᔒ荨䉦ᘀ慨え㔀脈⡯ḁံ჊ᅶᅸᅺᇄሪሬቌከጆገጊጌጔ጖ጸᎆᏔᏸᐰᑢᑤᒎᓎᓐýﴀýﴀýﴀñññññÝ�Ý�Ý�Ý�Ý̀$␷㠀$⑈愀$摧䍽_܀␃愁Ĥ摧⢶X̀$␷㠀$⑈愀$摧畺 Āᤀᅶᆀᆘᆜᆨᆮᇀᇂᇄᇠሦረሪቈቊቌኌኦከ�쓎캺躤玤䕘ᔤ穨ꁵᘀ穨ꁵ䌀ᡊ䬀H伀ъ儀ъ洀၈猄၈ᔵ穨ꁵᘀ穨ꁵ䈀ପ䩃䡋䩏䩑䩞䩡䡭А桰謢"䡳Аᔵ穨ꁵᘀ穨ꁵ䈀Ī䩃䡋䩏䩑䩞䩡䡭А桰䡳Аᘪ⩨搇䈀Ī䩃䡋䩏䩑䩞䩡⡯瀁hᘪ穨ꁵ䈀Ī䩃䡋䩏䩑䩞䩡⡯瀁hᔒ荨䉦ᘀ穨ꁵ㔀脈⡯ᔒ荨䉦ᘀ捨豎㔀脈⡯ᔒ荨䉦ᘀ佨昻㔀脈⡯ᔒ荨䉦ᘀ穻㔀脈⡯ᔒ荨䉦ᘀ≌㔀脈⡯ᔒ荨䉦ᘀ襨큭㔀脈⡯ᔒ荨䉦ᘀ恔㔀脈⡯ሁከዦጄጆገጊጌጎጔ጖ጴጶጸ፼ퟫꯁ辞満岏届6ᘧ絨彃䈀Ī䩃䡋䩏䩑䩞䩡桰ᔢ荨䉦ᘀ泌牖㔀脈䩃䡋䩏䩑⡯ᔢ荨䉦ᘀ絨彃㔀脈䩃䡋䩏䩑⡯ᔣ뙨堨ᘀ뙨堨㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘝ뙨堨㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘜ뙨堨㔀脈䩃䡋䩏䩑⡯ᘙ絨彃䌀ᡊ䬀H伀ъ儀ъ漀Ĩᘪ絨彃䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᘪ穨ꁵ䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᘧ穨ꁵ䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘧ穨ꁵ䈀Ī䩃䡋䩏䩑䩞䩡桰ഀ፼ᎄᎆᏊᏒᏔ᏶ᏸᐮᐰᑠᑢᑤᒎᒔᒚᒤᓌᓎᓐᓒ�쯟쯟쯟ꢵ蒖橸橜㵓ᘪ荨䉦䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᘑ荨䉦䌀ᡊ䬀H漀Ĩᔚ荨䉦ᘀ䱨�㔀脈䩃䡋⡯ᔚ荨䉦ᘀ롚㔀脈䩃䡋⡯ᔗ荨䉦ᘀ롚㔀脈䩃䡋ᔢ荨䉦ᘀ롚㔀脈䩃䡋䩏䩑⡯ᔢ荨䉦ᘀ譨♯㔀脈䩃䡋䩏䩑⡯ᘙ譨♯䌀ᡊ䬀H伀ъ儀ъ漀Ĩᘪ絨彃䈀Ī䩃䡋䩏䩑䩞䩡⡯瀁hᘧ絨彃䈀Ī䩃䡋䩏䩑䩞䩡桰ᘖ絨彃䌀ᡊ䬀H伀ъ儀ъᘧ絨彃䈀ପ䩃䡋䩏䩑䩞䩡桰謢"᐀ᓐᓒᓔᓜᓞᔐᔲᕔᕶᖘᖚᖶᗠᘥᘺᙎᙵᚉᚾᛋᛳ᜛ᝏ᝸ឣóëóóóó�ß�ß�ß�ß�ß�ß�̀$␷㠀$⑈愀$摧塲?܀␃愁Ĥ摧ိÃ̀$␷㠀$⑈愀$摧暃B᠀ᓒᓔᓖᓜᓞᓪᓮᓴᓼᔎᔐᔰᔲᕒᕔᕴᕶᕼᖖᖘᖚᖶᖾ룄룄룄颤颤颤炄掘㵑ᘧ牨㽘䈀Ī䩃䡋䩏䩑䩞䩡桰ᔢ蕨ิᘀ蕨ิ㔀脈䩃䡋䩏䩑⡯ᘙ荨䉦䌀ᡊ䬀H伀ъ儀ъ漀Ĩᘧ荨䉦䈀Ī䩃䡋䩏䩑䩞䩡桰ᘧ荨䉦䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘖ荨䉦䌀ᡊ䬀H伀ъ儀ъᘧ荨䉦䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᔗ齨ᘀ荨䉦㔀脈䩃䡋ᔛ齨ᘀ荨䉦㔀脈䩃䡋䩑ᔣ뙨堨ᘀ⵨쌐㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘝ⵨쌐㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘘ⵨쌐㔀脈䩃䡋䩑⡯ᘁᖾᗞᗠᗦᘤᘥᘩᘹᘺᘽᙀᙉᙍᙎᙔᙖᙟᙴᙵᙾᚁᚈᚉᚹᚽᚾᛇᛊᛋᛑᛕᛮᛲᛳ᜖᜚᜛ᝊᝎᝏᝳ᝷᝸សអឣ᠀᠐ᢘᢚᢴ�쯟�럋쯟쮷�럋�쯟�럋쯟�쯟�ꯟ鞡薎ᘐᝨ윪㔀脈䩃⡯ᘐ穨ꁵ㔀脈䩃⡯ᔓ器ᘀ٨က㔀脈䩃ᔓ器ᘀ蕨ิ㔀脈䩃ᔗ牨㽘ᘀ荨䉦䌀ᡊ䬀H漀Ĩᘧ牨㽘䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘧ牨㽘䈀Ī䩃䡋䩏䩑䩞䩡桰ᘖ牨㽘䌀ᡊ䬀H伀ъ儀ъᘧ牨㽘䈀ପ䩃䡋䩏䩑䩞䩡桰謢"㈀ឣឤᢚᤀᤂᤄᦖ᧮ᩎ᪠᫶᫸᫺᫼ᬄᬆᰌᰎ᱂᲎᳂ᳬᴦᷠḕóñååååå�åå턀Ñ턀Ñ턀Ñ턀̀$␷㠀$⑈愀$摧撸ø܀␃愁Ĥ摧砫Ñ̀$␷㠀$⑈愀$摧ÿ#Ā̀$␷㠀$⑈愀$摧䍽_᠀ᢴᢶᢸᣢᣤᣦᣨᣪᤀᤄᤨᤪ᤬ᥖᥘᥚᥜᥞᦀᦔᦖ샑ꆳ粌粡乥ꆌꄿᘜｨ⌀㔀脈䩃䡋䩏䩑⡯̬�ᔀｨ⌀ᘀｨ⌀㔀脈䩃䡅￶䡋䩏䩑ࡕ̭魪�੎Ĉ栕ÿ#栖ÿ#࠵䎁ᑊ䬀H唀Ĉࡖ愁ᑊ漀Ĩᔟｨ⌀ᘀｨ⌀㔀脈䩃䡋䩏䩑̨jᔀｨ⌀ᘀｨ⌀㔀脈䩃䡋䩏䩑ࡕᔢｨ⌀ᘀｨ⌀㔀脈䩃䡋䩏䩑⡯ᘙｨ⌀䌀ᡊ䬀H伀ъ儀ъ漀Ĩ̠繪ᔀᝨ윪ᘀᝨ윪㔀脈䩃䡅￴ࡕ̤ժ�੎Ĉ栖⨗Ç䩃䡋ࡕ嘁Ĉ䩡⡯ᘐᝨ윪㔀脈䩃⡯ᘍᝨ윪㔀脈䩃̖jᘀᝨ윪㔀脈䩃ࡕᐁᦖ᧜᧬᧮ᩌᩎ᪖᪞᪠᫮᫴᫸᫺᫼᫾ᬄᬆ᭔ᮈᯨᰊᰌퟫ쯗ퟫꢵ貛魺摯䡕=ᘕh䔘䌀ᡊ䬀H儀ъ漀Ĩᔘh䔘ᘀh䔘䌀ᡊ䬀H儀ъᔝh䔘ᘀh䔘䈀ପ䩃䡋桰謢"ᔔh䔘ᘀh䔘䌀ᡊ䬀Hᔔh䔘ᘀ赨제䌀ᡊ䬀Hᔣ뙨堨ᘀ⭨텸㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘝ⭨텸㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘙ⭨텸䌀ᡊ䬀H伀ъ儀ъ漀Ĩᘙｨ⌀䌀ᡊ䬀H伀ъ儀ъ漀Ĩᘪｨ⌀䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᘖｨ⌀䌀ᡊ䬀H伀ъ儀ъᘧｨ⌀䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘧｨ⌀䈀Ī䩃䡋䩏䩑䩞䩡桰ᔀᰌᰎᰠ᱀᱂᱔᲌᲎Რ᳀᳂ᳪᳬ᳾ᴄᴜᴤᴦᷖᷞᷠḔḕḡḣḹṇṈṩṪṶṺṻẍẎẾề�ꪽ뷘�誖詶扶陶皊誖詶扶陶皊皊癢誖陶ᘧ롨䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘧ롨䈀Ī䩃䡋䩏䩑䩞䩡桰ᘖ롨䌀ᡊ䬀H伀ъ儀ъᘧ롨䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᔤ롨ᘀ롨䌀ᡊ䬀H伀ъ儀ъ洀၈猄၈ᔵ롨ᘀ롨䈀ପ䩃䡋䩏䩑䩞䩡䡭А桰謢"䡳Аᔵ롨ᘀ롨䈀Ī䩃䡋䩏䩑䩞䩡䡭А桰䡳Аᔗh䔘ᘀh䔘䌀ᡊ䬀H漀Ĩ␀ḕṈṪẎỂỒởἒἯᾅᾒῡ․⁴⃖K⅌⇺∰≠⋀⋶⍘⎤⏚⏜⏞⏠óóóóóóóóóñññññĀ̀$␷㠀$⑈愀$摧撸øᬀềỂỎốỒớỞởἎἑἒἛἝἥἮἯὩᾄᾅᾎᾑᾒΉῠῡΏ•․⁔⁲⁴₤⃔⃖ℌℨK⅄ⅆⅈ⅌�뻊쫞�뺪쫞꫞�뺪쫞�뺪꫞�钪꫞�钪窆涆ᘘ⭨ሃ㔀脈䩃䡋䩑⡯ᔗ赨�ᘀ㭨ꄓ㔀脈䩃䡋ᔛ赨�ᘀ㭨ꄓ㔀脈䩃䡋䩑ᘪ롨䈀ପ䩃䡋䩏䩑䩞䩡⡯瀁≨⊋ᘧ롨䈀ପ䩃䡋䩏䩑䩞䩡桰謢"ᘖ롨䌀ᡊ䬀H伀ъ儀ъᘧ롨䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿᘧ롨䈀Ī䩃䡋䩏䩑䩞䩡桰ᘙ롨䌀ᡊ䬀H伀ъ儀ъ漀Ĩ⠀⅌⅖⅜ⅶↀↈ←→↸⇐⇪⇶⇸⇺⇾∮∰∴∾≖≜≞≠⌞⌠⌢⍌⍎⍐췴듀충邙纇螐螐螐犐遫填̤㉪�੎Ĉ栖㏳䩃䡋ࡕ嘁Ĉ䩡⡯ᘍḳ㔀脈䩃̖jᘀḳ㔀脈䩃ࡕᘐｨ⌀㔀脈䩃⡯ᘐ䭨쵷㔀脈䩃⡯ᘐḳ㔀脈䩃⡯ᔞ⭨ሃᘀ⭨ሃ㔀脈䩃䡋䩑⡯ᘔ䭨쵷㔀脈䩃䡋⡯ᔗ赨�ᘀ䭨쵷㔀脈䩃䡋ᘘ䭨쵷㔀脈䩃䡋䩑⡯ᘘ⭨ሃ㔀脈䩃䡋䩑⡯ᔗ赨�ᘀ㭨ꄓ㔀脈䩃䡋ᔛ赨�ᘀ㭨ꄓ㔀脈䩃䡋䩑ᘕ⭨ሃ㔀脈䩃䡋䩑ᰀ⍐⍒⍔⍘⍬⍮⍰⎚⎜⎞⎠⎢⎤⏚⏠⏢⏨⏪刀削剜퇚뻅뻑骫퇅袑杹属䢈ᘧ퉨䈀Ī䩃䡋䩏䩑䩞䩡桰唃Ĉᘐၨｏ㔀脈䩃⡯ᔣ뙨堨ᘀၨｏ㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘝၨｏ㔀脈⩂䌆ⱊ愀ⱊ漀Ĩ桰ÿᘐ퉨㔀脈䩃⡯ᘐ㔀脈䩃⡯̠㍪ᔀ靨찂ᘀ靨찂㔀脈䩃䡅￸ࡕ̤卪�੎Ĉ栖ʗÌ䩃䡋ࡕ嘁Ĉ䩡⡯ᘍ靨찂㔀脈䩃̖jᘀ靨찂㔀脈䩃ࡕᘐ靨찂㔀脈䩃⡯ᘐḳ㔀脈䩃⡯̖jᘀḳ㔀脈䩃ࡕ̠�ᔀḳᘀḳ㔀脈䩃䡅￶ࡕᐁ⏠⏨⏪削劔勮厚各周哎唌啈嗎噌噬囔圂圖圤垎堖堾塞塲墀壔壖壘÷õééééééééééõõ̀$␷㠀$⑈愀$摧ᣒõĀ܀␃愁Ĥ摧伐ÿᬀ这部分对应于迭代终止判断，没有相应公式可以写，只是判断终止条件是否满足，
         % END OF ESTIMATE OF SIGNAL
         for j=1:ln   % to send next message
            pdf_tmp=reshape(pdf_M_to_N(neighbors(j),self_index(j),:),1, model_order);
            pdf_tmp=pdf_tmp+epsilon; % for stability
            [pdf_tosend]=divpdf(pdf_res,pdf_tmp);
            pdf_tosend=pdf_tosend/sum(pdf_tosend);
            tmptmp=pdf_tosend;
            if (it>1) % MDBPF
               prevpdf=reshape(pdf_N_to_M(i, j,:),1,model_order);;
               tmptmp=gmean(pdf_tosend,prevpdf,gamma_mdbpf,0);
            end
            pdf_N_to_M(i, j, :)=tmptmp/sum(tmptmp);
         end %of for j
      end
   end
   if (it >=2) % display and break on last iteration
      dispvec_anderrors(mrecon, phi, phisign, measvec, dispind, x);
      if (it==iter)
         break;
      end
   end
其中，函数divpdf.m也很简单，就是返回pdf_res除以pdf_tmp的值。

七部分

下面是程序的最后一部分，即信息从变量节点传到测量节点。若为第一次迭代，则程序从初始化pdf_N_to_M(i, rr, :)=pdf_prior(:);后就进步本循环。

    %---------------
   % BACKWARD ITERATION - from signal to measurements
    %---------------
   for i=1:m
      neighbors=phi(i,:);
      neighbors=setdiff_shri(neighbors,0);
      ln=length(neighbors);
      phisigni=phisign(i,1:ln);
      self_index=self_indexM(i,:);
      pdf_res_all=[];
      for jj=1:ln % process neighbors
         tmptmp=[reshape(pdf_N_to_M(neighbors(jj),self_index(jj),:),1, model_order)];
         if ((phisigni(jj) < 0) & (b1))
            tmptmp=reverse(tmptmp,model_order);
         end
         if (length(pdf_res_all)==0) % first time
            pdf_res_all=(fft((tmptmp)));
            pdf_res_all=pdf_res_all+epsilon;
         else
            pdf_res_all=convpdf_fft(pdf_res_all, tmptmp, epsilon);
         end
      end
      if (sigma_Z>epsilon)
         [pdf_res_all]=convpdf_fft(pdf_res_all, y_noise, epsilon);
      end
      for j=1:ln   %To send next message
         tmptmp=[reshape(pdf_N_to_M(neighbors(j),self_index(j),:),1, model_order)];
         mvi=measvec(i);
         if ((phisigni(j) < 0) & (b2))
            tmptmp=reverse(tmptmp,model_order);
         end
         pdf_res=unconvpdf_fft(pdf_res_all, tmptmp, epsilon);
         pdf_res=abs((ifft((pdf_res))));
         pdf_res=shiftpdf_fft(pdf_res, mvi, delta, model_order);
         pdf_res=pdf_res/sum(pdf_res);
         if ((phisigni(j) < 0) & (b3)) % MDPB
            pdf_res=reverse(pdf_res,model_order);
         end
         tmptmp=pdf_res;
         if (it>1) % MDBPF
            prevpdf=reshape(pdf_M_to_N(i, j, :), 1, model_order);;
            tmptmp=gmean(pdf_res, prevpdf, gamma_mdbpb,0);
         end
         pdf_M_to_N(i, j, :)=tmptmp/sum(tmptmp);
      end
   end
以上部分其实就对应于公式（4）
