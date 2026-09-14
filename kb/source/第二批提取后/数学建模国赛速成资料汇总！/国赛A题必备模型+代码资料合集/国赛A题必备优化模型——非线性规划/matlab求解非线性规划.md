1.求解非线性规划
min	 EMBED Equation.DSMT4
s.t.		 EMBED Equation.DSMT4
		 EMBED Equation.DSMT4
		 EMBED Equation.DSMT4
		-2.3 EMBED Equation.DSMT4  2.3	i=1,2
-2.3 EMBED Equation.DSMT4  3.2	i=3,4,5
(1)代码如下
fun1.m
function f=fun1(x)
㵦硥⡰⡸⤱砪㈨⨩⡸⤳砪㐨⨩⡸⤵㬩഍潣瑮洮昍湵瑣潩⁮䝛䜬煥㵝潣瑮砨ഩ㵇嵛഻敇㵱硛ㄨ帩⬲⡸⤲㉞砫㌨帩⬲⡸⤴㉞砫㔨帩ⴲ〱砬㈨⨩⡸⤳㔭砪㐨⨩⡸⤵砬ㄨ帩⬳⡸⤲㍞ㄫ㭝഍整瑳洮砍㴰ㅛㄬㄬㄬㄬ㭝䄍嬽㭝㵢嵛഻敁㵱嵛戻煥嬽㭝氍㵢ⵛ⸲ⰳ㈭㌮⴬⸲ⰳ㈭㌮⴬⸲崳画㵢㉛㌮㈬㌮㌬㈮㌬㈮㌬㈮崬഻硛攬楸晴慬Ⱨ癦污㵝浦湩潣⡮晀湵ⰱへ䄬戬䄬煥戬煥氬Ɫ扵䀬潣瑮ഩ
(2)执行结果如下
Warning: Large-scale (trust region) method does not currently solve this type of problem,
 switching to medium-scale (line search).
> In fmincon at 274
  In test at 5
Optimization terminated: magnitude of directional derivative in search
 directi؀ࠔࠜࠞࠠࡊࡌࡎࡐࡒࡠࡢࡤࢎ࢐࢒࢔࢖࢜࢞ࢠ࣐࣒࣊࣌࣎ࣘࣚࣜआई쳗쳦ꖶ쳗쳦纏쳗쳦坨쳗쳦̡艪ᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪⵪㲸ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯̡ᥪᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪ᵪ㲸ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯̡jᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪ﭪ㲷ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯ᔔѨŦᘀ恨䤽䌀᱊愀᱊̝jᔀѨŦᘀ恨䤽䌀᱊唀Ĉ䩡ᔗѨŦᘀ恨䤽䌀᱊愀᱊漀ĨᔚѨŦᘀ恨䤽㔀脈䩃䩡⡯ḁ؀ࠔࡔ࢘ࣔऐ०়ৌ৚਀ਡਢ਩ੂੈછજણળા્ଆୂୃఔೈú切ú切ú切í切úá切úáú切ááá切ú切̀$␷㠀$⑈愀$摧㵠Iఀ萏Ƥ萑Ƥ葞Ƥ葠Ƥ摧㵠IЀ摧㵠Iᨀ؀᮪þĂāईऊऌऎजञठॊौॎॐ॒८॰ঞঠঢত঺়৊৚뻊돊뎾貝뻊돊敶뻊乜Cᘔ恨䤽㔀脈䩃䩡⡯ᔚѨŦᘀ恨䤽㔀脈䩃䩡⡯ᘑ恨䤽䌀᱊愀᱊漀Ĩ̡幪ᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪ꍪ㲸ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯̡襪ᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪齪㲸ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯ᔔѨŦᘀ恨䤽䌀᱊愀᱊ᔗѨŦᘀ恨䤽䌀᱊愀᱊漀Ĩ̝jᔀѨŦᘀ恨䤽䌀᱊唀Ĉ䩡̡虪	ᔀѨŦᘀ恨䤽䌀᱊䔀嗿Ĉ䩡̪㱪㲸ੑĈ栕昄栖㵠I䩃䡋ࡕ嘁Ĉ䩡⡯ᔁ৚৪৾਀ਠਡ਩਱ੁੂੇੈચછણલળઽાૌ્ଅଆୁୂఔ฀ᨀ᪼᫪᫬᫲᫴᭘᭚᭮᭰ᮄᮆᮒᮔᮠᮢᮦᮨ᮪ퟫퟋ샋ퟫퟋퟋ샋쯗쯗쯗쯗쯗듀뒲鮩鮩鮴鮩鮴鮩鮩살ᘆ恨䤽ᔚѨŦᘀ恨䤽㔀脈䩃䩡⡯ᘑ恨䤽㔀脈䩃䩡唃ĈᔗѨŦᘀ恨䤽㔀脈䩃䩡ᘔ恨䤽㔀脈䩃䩡⡯ᘖ恨䤽䌀ᡊ䬀H伀͊儀͊ᘧ恨䤽䈀Ī䩃䡋䩏䩑䩞䩡桰ᘧ恨䤽䈀Ȫ䩃䡋䩏䩑䩞䩡桰ÿⴀೈജൄൢ෰᩾᪼᫬᫴᭚᭰ᮆᮔᮢᮨ᮪ú切ú切ú切ú切ú切ú切ú切øĀЀ摧㵠Iༀon less than 2*options.TolFun and maximum constraint violation
  is less than options.TolCon.
No active inequalities.
x =
   -1.7172    1.5957    1.8272    0.7640    0.7633
exitflag =
    0.0539
fval =
     5
>>
