
#2. Prezentarea bazei de date

#importarea bazei de date
import pandas as pd
bd = pd.read_csv('ESS10NO.csv')

#prezentarea bazei de date initiale
bd.dtypes
len(bd)
len(bd.columns)

#Redenumirea coloanelor
bd.columns = ["rownames", "country", "id", "region", "int_start", "int_end", "dweight", 
             "pspwght", "pweight", "anweight", "prob", "stratum", "psu", "eu_vote", 
             "born_NO", "age", "img_econ", "img_culture", "img_bptl", "female", 
             "educ_yrs", "unemployed", "pol_interest", "household_income", "lrscale"]

#Crearea unei variabile categoriale "img_bptl_fact" bazate pe variabila numerica "img_bptl"
interval = [-1, 3, 6, 10]
etichete = ['Low Tolerance', 'Medium Tolerance', 'High Tolerance']
bd['img_bptl_fact'] = pd.cut(bd['img_bptl'], interval, labels = etichete) 

#Alegerea variabilelor ce urmează sa fie folosite in proiect având in vedere
# numărul  de valori  lipsa si valorile eronate
bd.isna().sum()

# Din baza de date selectata voi folosi variabilele numerice:
# - img_bptl, aceasta variabila a fost aleasa in detrimentul 'img_econ' intrucat contine mai putine valori lipsa
# - age, a fost aleasa pentur ca nucontine valori lipsa
# - educ_yrs, a fost aleasa in detrimentul variabilei 'household_income' intrucat prezinta mai putine valori lipsa
# si variabilele nenumerice
# - img_bptl_fact
# - eu_vote

#Operații preliminare
#1. Din baza inițială se va face o selecție care să includă condiții pentru cel puțin două variabile.
#Cerințele proiectului vor fi executate pentru această selecție.
bd = bd[bd['born_NO'] == 1]
bd = bd[bd['pol_interest'] == 1]
bd = bd[['img_bptl', 'age', 'educ_yrs', 'img_bptl_fact', 'eu_vote']]
#2. Noua baza va fi exportată și folosită în analiză.
bd.to_excel('bd.xlsx')
#3. Toate variabilele categoriale să aibă categoriile definite.
bd.dtypes
bd['eu_vote'] = pd.Categorical(bd['eu_vote'])
bd['eu_vote'].cat.categories
bd['img_bptl_fact'].cat.categories

# Prezentarea bazei de date finale
bd.dtypes
len(bd)
len(bd.columns)
bd['eu_vote'].cat.categories
bd['img_bptl_fact'].cat.categories

#3. Analiza grafică și numerică a variabilelor analizate

#analiza descriptivă a variabilelor numerice și nenumerice;
bd.describe(include = 'all')

from scipy.stats import skew
from scipy.stats import kurtosis
skew(bd['age'])
skew(bd['img_bptl'], nan_policy='omit')
skew(bd['educ_yrs'], nan_policy='omit')

kurtosis(bd['age'])
kurtosis(bd['img_bptl'], nan_policy='omit')
kurtosis(bd['educ_yrs'], nan_policy='omit')


#analiza grafică a variabilelor numerice și nenumerice;
import matplotlib.pyplot as plt
import seaborn as sns

# Variabile numerice
#histograme
sns.histplot(
    data = bd,
    x = 'img_bptl')

sns.histplot(
    data = bd,
    x = 'age')

sns.histplot(
    data = bd,
    x = 'educ_yrs')

#barploturi
sns.countplot(
    data = bd,
    x = 'eu_vote')
plt.xticks(rotation=45) 
plt.show()

sns.countplot(
    data = bd,
    x = 'img_bptl_fact')
plt.xticks(rotation = 45)
plt.skow()

#- identificarea outlierilor și tratarea acestora.

# Boxplot-urile nu ppot fi create pentru variabile de tip float si variabile care contin nan-uri, 
#asa ca am creat 3 obiecte noi pentru a putea crea boxploturile
import numpy as np
age = [int(x) for x in bd['age'] if not np.isnan(x)]
educ_yrs = [int(x) for x in bd['educ_yrs'] if not np.isnan(x)]
img_bptl = [int(x) for x in bd['img_bptl'] if not np.isnan(x)]

fig, ax = plt.subplots()
ax.boxplot([img_bptl, age, educ_yrs])
ax.xaxis.grid(True)
ax.set_xticklabels(['img_bptl', 'age', 'educ_yrs'])


#4. Analiza statistică a variabilelor categoriale
# tabelarea datelor;
tabel = pd.crosstab(bd['eu_vote'], bd['img_bptl_fact'])

#frecv marginala
frecv_marg_eu_vote = tabel.sum(axis = 1)
frecv_marg_img_bptl_fact = tabel.sum()

#frecv conditionate
frecv_conditionata = (tabel / frecv_marg_img_bptl_fact) * 100

#frecv partiala
tabel.loc["Wouldn't Vote", 'High Tolerance']
tabel.loc['Refuse to Answer', 'High Tolerance']
tabel.loc['Not Eligible', 'Medium Tolerance']

# analiza de asociere;
from scipy.stats import chi2_contingency
from scipy.stats import chisquare
chi2_contingency(tabel)
#pvalue=0.03937

# analiza de concordanță.
observate = bd['img_bptl_fact'].value_counts()
numar_categorii = len(observate)
total_observatii = len(bd)
asteptate = np.array([total_observatii / numar_categorii] * numar_categorii)
chisquare(observate, np.sum(observate)/np.sum(asteptate) * asteptate)
#pvalue=1.024702510591034e-55


observate2 = bd['eu_vote'].value_counts()
numar_categorii2 = len(observate2)
asteptate2 = np.array([total_observatii / numar_categorii2] * numar_categorii2)
chisquare(observate2, np.sum(observate2)/np.sum(asteptate2) * asteptate2)
#pvalue=0.0

#5. Estimarea și testarea mediilor
#- estimarea mediei prin interval de încredere;
import scipy as sp
import scipy.stats
def IC (data, incredere):
    a = 1.0*np.array(data)
    n = len(a)
    media = np.mean(a)
    sem = scipy.stats.sem(a)
    h = sem * sp.stats.t.ppf((1 + incredere)/2.,
                              n-1)
    return media-h, media+h

IC(educ_yrs, 0.95)
# [15.113785627119892, 15.682102772292737]

#testarea mediilor populației: testarea unei medii cu o valoare fixă; testarea diferenței dintre
#două medii (eșantioane independente sau eșantioane perechi); testarea diferenței dintre trei
#sau mai multe medii.

#testarea mediei cu o valoare fixa
import scipy.stats as stats
stats.ttest_1samp(educ_yrs, 12, alternative= 'greater')
#pvalue=4.927408677743371e-90

#testarea diferentei dintre 2 medii

#Test de omogenitate a variantelor
Join_EU = bd[bd['eu_vote'] == 'Join EU']['educ_yrs']
Join_EU = [x for x in Join_EU if not np.isnan(x)]
Remain_Outside = bd[bd['eu_vote'] == 'Remain Outside']['educ_yrs']
Remain_Outside = [x for x in Remain_Outside if not np.isnan(x)]
from scipy.stats import levene
levene(Join_EU, Remain_Outside) 
#pvalue=0.07763

#Testarea diferentei dintre cele 2 medii
stats.ttest_ind(Join_EU, Remain_Outside, equal_var= True)
# pvalue=0.0028 


# Testarea diferentelor dintre 3 medii
import statsmodels.formula.api as smf
model = smf.ols('educ_yrs ~ img_bptl_fact', data = bd).fit()
import statsmodels.api as sms
sms.stats.anova_lm(model, type = 2)
#p-value =0.0001 < 0.01

#6. Analiza de regresie și corelație
#- matricea de corelatie
bd_num = bd.drop(bd.columns[[3, 4]], axis=1)
bd_num.corr()

# teste de corelatie
bd_clean = bd.dropna()
stats.pearsonr(bd_clean['img_bptl'], bd_clean['age'])
#pvalue=0.0011

stats.pearsonr(bd_clean['img_bptl'], bd_clean['educ_yrs'])
#pvalue=1.4036734366748627e-06

# analiza de regresie: regresie liniară simplă, regresie liniară mutiplă și regresie neliniară;


# Regresia simpla
simp_reg = smf.ols('img_bptl ~ educ_yrs', data = bd).fit()
print(simp_reg.summary())
err_simp_reg = simp_reg.resid
fit_simp_reg = simp_reg.fittedvalues
#   (Intercept)       educ_yrs
#    5.03221761     0.09790771


# crearea plotului
print(plt.scatter(bd['educ_yrs'], bd['img_bptl']))
sns.regplot(x ='educ_yrs', y='img_bptl', data=bd, ci=None,
            line_kws={'color': 'red'})


# Regresia multipla
mult_reg = smf.ols('img_bptl ~ educ_yrs + age', data = bd).fit()
print(mult_reg.summary())
err_mult_reg = mult_reg.resid
fit_mult_reg = mult_reg.fittedvalues
#  (Intercept)     educ_yrs        age 
#  5.77413019    0.09115558    -0.01208034

#Regresie neliniara
bd['educ_yrs_sq'] = bd['educ_yrs'] ** 2
nonl_reg = ols('img_bptl ~ educ_yrs + educ_yrs_sq', data = bd).fit()
print(nonl_reg.summary())
err_nonl_reg = nonl_reg.resid
fit_nonl_reg = nonl_reg.fittedvalues
#  (Intercept)        educ_yrs       educ_yrs_sq
#  6.099205340     -0.058222421      0.005319936

# Generează puncte pentru linia de regresie
x_lin = np.linspace(bd['educ_yrs'].min(), bd['educ_yrs'].max(), 100)
y_lin = nonl_reg.params[0] + nonl_reg.params[1] * x_lin + nonl_reg.params[2] * x_lin**2
plt.scatter(bd['educ_yrs'], bd['img_bptl'])
plt.plot(x_lin, y_lin, color='red')

#- testare ipoteze;
 # 1. media erorilor este 0

stats.ttest_1samp(err_simp_reg, 0) #pvalue=0.999
stats.ttest_1samp(err_mult_reg, 0) #pvalue=0.999
stats.ttest_1samp(err_nonl_reg, 0) #pvalue=0.999
#toate modelele indeplinesc ipoteza conform careia media erorilor trebuie sa fie 0


# crearea ploturilor
plt.figure(figsize = (8, 6))
sns.scatterplot(x = fit_simp_reg, y = err_simp_reg,
                color = 'blue')
plt.axhline(0, color = 'red', linestyle = '--')
plt.title('Erori vs Valori Ajustate pentru simp_reg')
plt.xlabel('Valori Ajustate')
plt.ylabel('Erori')
plt.show()

plt.figure(figsize = (8, 6))
sns.scatterplot(x = fit_mult_reg, y = err_mult_reg,
                color = 'blue')
plt.axhline(0, color = 'red', linestyle = '--')
plt.title('Erori vs Valori Ajustate pentru mult_reg')
plt.xlabel('Valori Ajustate')
plt.ylabel('Erori')
plt.show()


plt.figure(figsize = (8, 6))
sns.scatterplot(x = fit_nonl_reg, y = err_nonl_reg,
                color = 'blue')
plt.axhline(0, color = 'red', linestyle = '--')
plt.title('Erori vs Valori Ajustate pentru mult_reg')
plt.xlabel('Valori Ajustate')
plt.ylabel('Erori')
plt.show()

# 2. ipoteza de normalitate
stats.jarque_bera(err_simp_reg)
#pvalue=0.06125 norm
stats.jarque_bera(err_mult_reg)
#pvalue=0.0330 ne-norm
stats.jarque_bera(err_nonl_reg)
#pvalue=0.0566 norm 

 # 3. ipoteza de heteroscedasticitate

from statsmodels.stats.diagnostic import het_breuschpagan
het_breuschpagan(err_simp_reg, simp_reg.model.exog)
#p-value = 0.0316 hetero 

het_breuschpagan(err_mult_reg, mult_reg.model.exog, robust= False)
# p-value = 0.0654 homo 

het_breuschpagan(err_nonl_reg, nonl_reg.model.exog)
#p-value = 0.3305 homo 

# 4 ipoteza de autocorelare a erorilor
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
acorr_breusch_godfrey(simp_reg)
#p-value = 0.9066 nu autocor
acorr_breusch_godfrey(mult_reg)
#p-value = 0.8822 nu autocor
acorr_breusch_godfrey(nonl_reg)
#p-value = 0.9071 nu autocor

# compararea a cel puțin 2 modele de regresie și alegerea celui mai potrivit model.
from  statsmodels.stats.anova import anova_lm
anova_lm(simp_reg, mult_reg)
# p-value = 0.006 mult-regeste semnificativ mai bun
