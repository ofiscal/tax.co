**********************************************************************
*   MOTRICO: Social Security Module and Income Tax                              *
*   Simulation of health,pensions, cajas de compensación, ICBF and SENA contributions using the ENPH 2016-2017
*   For 206-2017. For other periods variables have to be adjusted (future work)
*   Simulation of income tax using the ENPH 2016-2017
*   For 206-2017. For other periods variables have to be adjusted (future work)
*   Aproximation (the best data to run the microsimulation come from tax forms collected by DIAN. Pending)
*   Only for workers. Not possible to calculate for inactive population using this survey
*   Secondary job will be assumed as a one_month lump sum as we don't know duration for second job. No entry for second job is above minimum threshold to declare.
*********************************************************************
clear all
set trace off
set tracedepth 1
*set varabbrev off
set more on
macro drop _all
**********************

glo direct "C:\Users\David Suarez\Desktop\STATA\ENPH"
use "$direct\Caracteristicas_generales_personas.dta"

*El DANE genera primero la unidad de gasto...nosotros? Yo creo que es mejor hacer un análisis separado*
//El dane vuelve cero los ingresos de los miembros del hogar que no hacen parte de la unidad de gasto//
	
	
	recode P6050 (1=1 "Jefe") (2=2 "Conyuge") (3=3 "Hijo") (4 5 = 4 "Otro pariente") (9=5 "Otros no parientes") (6 7 8 = 6 "No UG") , gen(parentesco)

	tostring DIRECTORIO, replace
	gen hogares=DIRECTORIO  	

	generate ug = parentesco!=6
	
	tab ug
	
*Generate variable to distinguish employed, self-employed, unemployed and inactivos (main job).
gen fuerza_trabajo=.
replace fuerza_trabajo = 1 if (P6430==1| P6430==2|P6430==3|P6430==8)
replace fuerza_trabajo = 2 if (P6430==4| P6430==5|P6430==9)
replace fuerza_trabajo = 3 if (P6430==6| P6430==7)
replace fuerza_trabajo = 4 if P6350==1
replace fuerza_trabajo = 5 if P7472!=.
label define fuerza_trabajo 1 "Asalariado" 2 "Independiente" 3 "Trabajador sin Remuneración" 4 "Desempleado" 5 "Inactivo" 
label values fuerza_trabajo fuerza_trabajo

*Generate variable to distinguish employed, self-employed (secondary job).
gen fuerza_trabajo2=.
replace fuerza_trabajo2 = 1 if (P7050==1| P7050==2|P7050==3|P7050==8)
replace fuerza_trabajo2 = 2 if (P7050==4| P7050==5|P7050==9)
replace fuerza_trabajo2 = 3 if (P7050==6| P7050==7)
label define fuerza_trabajo2 1 "Asalariado" 2 "Independiente" 3 "Trabajador sin Remuneración" 
label values fuerza_trabajo2 fuerza_trabajo2


*Household Members
egen miembros_hogar=total(SECUENCIA_P==1), by(hogares)
egen miembros_asal=total(SECUENCIA_P==1 & fuerza_trabajo==1), by(hogares)
egen miembros_indep =total(SECUENCIA_P==1 & fuerza_trabajo==2),by(hogares)
egen miembros_no_rem=total(SECUENCIA_P==1 & fuerza_trabajo==3),by(hogares)
egen miembros_desoc =total(SECUENCIA_P==1 & fuerza_trabajo==4),by(hogares)
egen miembros_inac =total(SECUENCIA_P==1 & fuerza_trabajo==5),by(hogares)

table fuerza_trabajo [iw= FEX_C] //Ojo: Hay muchos inactivos según esta encuesta. La mayoría son inactivos porque responden que no quieren trabajar!! (Pregunta 6300)
//Overestimates asalariados: there are many earning below minimum wage

****Labor income aggregation (main job)****
*Asalariados: Making income from labor sources comparable, on a monthly basis. Inclusion of amounts conditional on P6500.

label define P6585S3A2 1 "Sí" 2 "No"
label values P6585S3A2 P6585S3A2

*label define P1653S1A2 1 "Sí" 2 "No"
*label values P1653S1A2 P1653S1A2
 
foreach x in 1 2 3 4 5 6 {
gen P6630S`x'A1_monthly= P6630S`x'A1/12
}
label drop P6510S2
replace P6510S2=0 if P6510S2==1
replace P6510S2=1 if P6510S2==2
label define P6510S2 0 "Sí" 1 "No"
label values P6510S2 P6510S2
gen P6510_check = P6510S1*P6510S2

foreach x in 1 2 3{
label drop P6585S`x'A2
replace P6585S`x'A2=0 if P6585S`x'A2==1
replace P6585S`x'A2=1 if P6585S`x'A2==2
label define P6585S`x'A2 0 "Sí" 1 "No"
label values P6585S`x'A2 P6585S`x'A2
gen P6585S`x'_check=P6585S`x'A1*P6585S`x'A2
}
foreach x in 1 2 3 4{
label drop P1653S`x'A2
replace P1653S`x'A2=0 if P1653S`x'A2==1
replace P1653S`x'A2=1 if P1653S`x'A2==2
label define P1653S`x'A2 0 "Sí" 1 "No"
label values P1653S`x'A2 P1653S`x'A2
gen P1653S`x'_check=P1653S`x'A1*P1653S`x'A2
}

*Independientes: 
gen P6750_monthly=P6750/P6760
gen P550_monthly=P550/12
//We include P6779S1 (travel expenses) as part of labor income for independendents (there are legal issues). The fulfillment insurance premium is an expenditure that has VAT (neglegible).

*
egen lbr_inc_monthly=rowtotal(P6500 P6510S1 P6590S1 P6600S1 P6610S1 P6620S1 P6585S1A1 P6585S2A1 P6585S3A1 *_check P1653S1A1 P1653S2A1 P1653S3A1 P1653S4A1 *_monthly P6779S1),missing
replace lbr_inc_monthly=lbr_inc_monthly-cond(missing(P6630S1A1_monthly), 0, P6630S1A1_monthly)
label variable lbr_inc_monthly "Monthly labor income. Main job"


****Labor income aggregation (for second job, unemployed and inactives)****  
*There is not much information.Ignore? The survey asked questions about more potential jobs, but they were not included in public datasets)
gen lbr_inc_monthly2= P7070
label variable lbr_inc_monthly2 "Monthly labor income. Secondary job"
egen lbr_inc_monthly3 = rowtotal(P7422S1 P7472),missing
label variable lbr_inc_monthly3 "Monthly labor income. Unemployed/Inactive"

*Adjusted income (control of 98/99)
foreach x in P6500 P6510S1 P6590S1 P6600S1 P6610S1 P6620S1 P6585S1A1 P6585S2A1 P6585S3A1 P1653S1A1 P1653S2A1 P1653S3A1 P1653S4A1 {
replace `x' =. if `x'==98 | `x'==99
}


foreach x in P6630S1A1 P6630S2A1 P6630S3A1 P6630S4A1 P6630S5A1 P6630S6A1 P6779S1 {
replace `x' =. if `x'==98 | `x'==99

}



foreach x in  P7422S1 P7472 P7070{
replace `x' =. if `x'==98 | `x'==99
}

replace P6750 = . if P6750==98 | P6750==99 
replace P550 =. if P550==99 



*******Social Security contributions*********
//No tax evasion/No tax avoidance 
//we will have to look at PILA data to better estimate frequency of contributions or mandatory contributions vis-à-vis actual contributions (UGPP)
//NOTE: These contributions are also called when calculating the taxable base for the income tax (annualized) 
//For second job, not enough information to convert to year. "Ingresos no constitutivos de renta" will be overestimated for people with more than one job... 
//For unemployed/inactive population,there is not enough information to annualize SSCs or regarding other sources of income. Their income tax will be calculated exclusively for extreme values (only one unemployed individual in the sample exceeds the threshold for income tax declaration. No inactive exceeds the threshold) assuming only labor income in previous periods.  	
//Includes contributions to health, pension, ICBF,SENA, Cajas de Compensacion. ARL not included by default in the simulation (info about what people do in their jobs is included in the survey, but it is not public)
//We assume that workers bear the tax, even though a portion of payroll taxes for asalariados comes from their employers (they transfer their part easily to employees in the form of lower wages, for instance)  	
//Salario Integral: Form of payment in Colombian Labor Law, exclusively for asalariados, that has a special treatment in terms of SSCs. We assume this form of payment if labor income is greater than 13 minimum wages.	
//Asalariados are always hired for a wage above or equal the minimum wage. Even if people report to be asalariados, we treat them as independent if they earn less than the minimum wage
//Social security for people receiving pensions will be considered in the income tax module.
	
	**Parameters:
	loc alfa 1                         //es la porcion de la prima técnica y demás que no hace parte del salario
	loc beta  1                         //es la porción de gastos de representación que no hacen parte del salario.
	loc gama  0                         //es la parte de los viáticos permanentes que no pertenecen al salario
	loc salario_minimo_2016 689500
	loc minimum_wage 737717             //Default is for 2017
	loc porcentaje_IBC_independientes 0.4
	loc cot_indep_pension 0.16
	loc cot_indep_health 0.125
	loc cot_asal_health 0.04
	loc cot_asal_pension 0.04
	loc cot_employer_health 0.085
	loc cot_employer_pension 0.12
	loc cot_employer_cajas 0.04        //parafiscales  
	loc cot_employer_sena 0.02        //parafiscales
	loc cot_employer_icbf 0.03
	loc salario_integral 0.7    //(0,7, mal definido en la ley)
	loc tope 25               //(25 salarios mínimos)
	loc piso_sintegral 13
	
	**Taxable Base (Ingreso Base de Cotización, IBC)
	//NOTE: Since the survey was carried on 2016 and 2017 and we don´t know the date observations were collected, we have problems for 6328 sample individuals (almost a million in the population) whose labor income was between the minimum wage of 2016 and the minimum of 2017. 
	//Same problem for the upper tail of labor incomes, although we only have 13 observations between 25 minimum wages for 2016 and 25 minimum wages for 2017.
	//Hack: Simulate three scenarios: excluding these observations; assuming the minimum wage of 2016; assuming the minimum wage for 2017 (used below); midpoint between the two. 
	//Real Solution: ask dane about collection dates (I know they have that info, it was in the preliminar version of the data)
	//By law, IBC could be between 40% and 100% of total labor income for independents. we assume IBC equals 40% of total labor income. TO DO: endogenous rates of contributions and taxable base for independent 
	//Data is not enough to come up with endogenous estimations of IBC for independents. Look at PILA data.

	
	gen IBC_mainjob=.
	gen IBC_secondjob=0
	replace IBC_mainjob = lbr_inc_monthly -cond(missing(P6585S1A1), 0, P6585S1A1)-cond(missing(P6585S2A1), 0, P6585S2A1)-cond(missing(P6585S3A1), 0, P6585S3A1)-cond(missing(P1653S1A1), 0, `alfa'*P1653S1A1)-cond(missing(P1653S3A1), 0,P1653S3A1)-cond(missing(P1653S4A1), 0, `beta'*P1653S4A1)-cond(missing(P6630S1A1_monthly), 0, P6630S1A1_monthly)-cond(missing(P6630S3A1_monthly), 0, P6630S3A1_monthly)-cond(missing(P6630S4A1_monthly), 0, `gama'*P6630S4A1_monthly)-cond(missing(P6630S6A1_monthly), 0, P6630S6A1_monthly) if fuerza_trabajo==1 
	
	replace IBC_mainjob = `salario_integral'*lbr_inc_monthly if (lbr_inc_monthly>`piso_sintegral'*`minimum_wage' & fuerza_trabajo==1)
	//Se supone, por falta de información, que los independientes no incurren en costos y gastos, por lo que su IBC no se ajusta.
	replace IBC_mainjob = `porcentaje_IBC_independientes'*lbr_inc_monthly if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
	replace IBC_mainjob = `minimum_wage' if IBC_mainjob<`minimum_wage'
	replace IBC_mainjob = `tope'*`minimum_wage' if IBC_mainjob>`tope'*`minimum_wage'
	replace IBC_secondjob = lbr_inc_monthly2 if fuerza_trabajo2==1
    replace IBC_secondjob = `salario_integral'*lbr_inc_monthly2 if lbr_inc_monthly2>`piso_sintegral'*`minimum_wage' & fuerza_trabajo2==1
	replace IBC_secondjob = `porcentaje_IBC_independientes'*lbr_inc_monthly2 if (fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage')
	replace IBC_secondjob = `minimum_wage' if IBC_secondjob<`minimum_wage'
	replace IBC_secondjob = `tope'*`minimum_wage' if IBC_secondjob>`tope'*`minimum_wage'
	//To ignore problematic observations:
	*replace IBC_mainjob =. if lbr_inc_monthly>`salario_minimo_2016' & lbr_inc_monthly<`minimum_wage'
	*replace IBC_secondjob =. if lbr_inc_monthly2>`salario_minimo_2016' & lbr_inc_monthly2<`minimum_wage'
	

	**Simulation
	gen health_mainjob_trabajador =.
	gen pension_mainjob_trabajador =.
	gen health_mainjob_employer =.
	gen pension_mainjob_employer=.
	gen parafiscales_mainjob =.
	gen cajas_mainjob =.
	gen health_secondjob_trabajador =.
	gen pension_secondjob_trabajador =.
	gen health_secondjob_employer =.
	gen pension_secondjob_employer=.
	gen parafiscales_secondjob =.
	gen cajas_secondjob =.
	

	//Variables that do not have parametric changes as a function of income beyond those implied for asalariados and independientes
	replace health_mainjob_trabajador=`cot_asal_health'*IBC_mainjob if fuerza_trabajo==1
	replace health_mainjob_trabajador=`cot_indep_health'*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
	replace pension_mainjob_employer=`cot_employer_pension'*IBC_mainjob if fuerza_trabajo==1
	replace cajas_mainjob=`cot_employer_cajas'*IBC_mainjob if fuerza_trabajo==1
	
	replace health_secondjob_trabajador=`cot_asal_health'*IBC_secondjob if fuerza_trabajo2==1
	replace health_secondjob_trabajador=`cot_indep_health'*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
	replace pension_secondjob_employer=`cot_employer_pension'*IBC_secondjob if fuerza_trabajo2==1
	replace cajas_secondjob=`cot_employer_cajas'*IBC_secondjob if fuerza_trabajo2==1
	
	
//Variables that do have parametric changes as a function of income 
*For main job
if lbr_inc_monthly<`minimum_wage'{
replace pension_mainjob_trabajador=0 if fuerza_trabajo==1
replace pension_mainjob_trabajador=0 if fuerza_trabajo==2
replace health_mainjob_employer=0*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=0*IBC_mainjob if fuerza_trabajo==1
}
else if (`minimum_wage'<=lbr_inc_monthly & lbr_inc_monthly<4*`minimum_wage') {
replace pension_mainjob_trabajador=`cot_asal_pension'*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=`cot_indep_pension'*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=0*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=0*IBC_mainjob if fuerza_trabajo==1
}
else if 4*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<16*`minimum_wage'{
if 4*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<10*`minimum_wage'{
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.01)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.01)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=0*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=0*IBC_mainjob if fuerza_trabajo==1
}
else{
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.01)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.01)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}

}
else if 16*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<17*`minimum_wage'{
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.012)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.012)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}
else if 17*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<18*`minimum_wage'{ 
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.014)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.014)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}
else if 18*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<19*`minimum_wage'{ 
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.016)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.016)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}
else if 19*`minimum_wage'<= lbr_inc_monthly & lbr_inc_monthly<20*`minimum_wage'{ 
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.018)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.018)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}
else {
replace pension_mainjob_trabajador=(`cot_asal_pension'+0.02)*IBC_mainjob if fuerza_trabajo==1
replace pension_mainjob_trabajador=(`cot_indep_pension'+0.02)*IBC_mainjob if fuerza_trabajo==2|lbr_inc_monthly<`minimum_wage'
replace health_mainjob_employer=`cot_employer_health'*IBC_mainjob if fuerza_trabajo==1
replace parafiscales_mainjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_mainjob if fuerza_trabajo==1
}
 *For second job
 if lbr_inc_monthly2<`minimum_wage'{
replace pension_secondjob_trabajador=0 if fuerza_trabajo2==1
replace pension_secondjob_trabajador=0 if fuerza_trabajo2==2
replace health_second job_employer=0*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=0*IBC_secondjob if fuerza_trabajo2==1
}
else if (`minimum_wage'<=lbr_inc_monthly2 & lbr_inc_monthly2<4*`minimum_wage') {
replace pension_secondjob_trabajador=`cot_asal_pension'*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=`cot_indep_pension'*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=0*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=0*IBC_secondjob if fuerza_trabajo2==1
}
else if 4*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<16*`minimum_wage'{
if 4*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<10*`minimum_wage'{
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.01)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.01)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=0*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=0*IBC_secondjob if fuerza_trabajo2==1
}
else{
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.01)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.01)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}

}
else if 16*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<17*`minimum_wage'{
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.012)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.012)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}
else if 17*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<18*`minimum_wage'{ 
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.014)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.014)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}
else if 18*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<19*`minimum_wage'{ 
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.016)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.016)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}
else if 19*`minimum_wage'<= lbr_inc_monthly2 & lbr_inc_monthly2<20*`minimum_wage'{ 
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.018)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.018)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}
else {
replace pension_secondjob_trabajador=(`cot_asal_pension'+0.02)*IBC_secondjob if fuerza_trabajo2==1
replace pension_secondjob_trabajador=(`cot_indep_pension'+0.02)*IBC_secondjob if fuerza_trabajo2==2|lbr_inc_monthly2<`minimum_wage'
replace health_secondjob_employer=`cot_employer_health'*IBC_secondjob if fuerza_trabajo2==1
replace parafiscales_secondjob=(`cot_employer_sena'+`cot_employer_icbf')*IBC_secondjob if fuerza_trabajo2==1
}

*Redefining independents according to our definition
gen fuerza_trabajo_our=.
replace fuerza_trabajo_our=1 if fuerza_trabajo==1
replace fuerza_trabajo_our=2 if fuerza_trabajo==2
replace fuerza_trabajo_our=2 if lbr_inc_monthly < 737717
replace fuerza_trabajo_our = 3 if (P6430==6| P6430==7)
replace fuerza_trabajo_our = 4 if P6350==1
replace fuerza_trabajo_our = 5 if P7472!=.
label define fuerza_trabajo_our 1 "Asalariado" 2 "Independiente" 3 "Trabajador sin Remuneración" 4 "Desempleado" 5 "Inactivo" 
label values fuerza_trabajo_our fuerza_trabajo_our
table fuerza_trabajo_our [iw= FEX_C]

egen miembros_asal_our=total(SECUENCIA_P==1 & fuerza_trabajo_our==1), by(hogares)
egen miembros_indep_our =total(SECUENCIA_P==1 & fuerza_trabajo_our==2),by(hogares)
egen miembros_norem_our=total(SECUENCIA_P==1 & fuerza_trabajo_our==3),by(hogares)
egen miembros_desoc_our =total(SECUENCIA_P==1 & fuerza_trabajo_our==4),by(hogares)
egen miembros_inac_our =total(SECUENCIA_P==1 & fuerza_trabajo_our==5),by(hogares)

foreach x in health_mainjob_trabajador pension_mainjob_trabajador health_mainjob_employer pension_mainjob_employer parafiscales_mainjob cajas_mainjob{
glo main_job = "$main_job `x'"
} 
foreach x in health_secondjob_trabajador pension_secondjob_trabajador health_secondjob_employer pension_secondjob_employer parafiscales_secondjob cajas_secondjob{
glo second_job = "$second_job `x'"
}
egen contribution_SSC_mainjob=rowtotal ($main_job ),missing
egen contribution_SSC_secondjob=rowtotal ($second_job ),missing
*Total cost to Employer: includes "prestaciones sociales" for asalariados below 13 minimum wages (Prima de servicios+cesantías+Intereses de Cesantías)
//: prestaciones sociales imply 2.12 extra earnings. We simulate according to time reported

generate prima_servicios_mainjob = .
generate cesantias_mainjob=.
generate intereses_cesantias_mainjob=.
generate prima_servicios_secondjob = .
generate cesantias_secondjob=.
generate intereses_cesantias_secondjob=.

if (lbr_inc_monthly<`piso_sintegral'*`minimum_wage' & fuerza_trabajo_our==1){

replace prima_servicios_mainjob = lbr_inc_monthly*(P6426/12) if P6426>0 &(P6040-(P6426/12))>10             //Checking age f worker and the time reported as working in current job. Excludes people that have worked less than a month
replace prima_servicios_mainjob = lbr_inc_monthly if P6426>12
replace prima_servicios_mainjob = prima_servicios_mainjob/12
replace cesantias_mainjob=lbr_inc_monthly*(P6426/12) if P6426>0 &(P6040-(P6426/12))>10
replace cesantias_mainjob=lbr_inc_monthly/12 if P6426>12
replace intereses_cesantias_mainjob=0.12*cesantias_mainjob
replace cesantias_mainjob = cesantias_mainjob/12
replace intereses_cesantias_mainjob=intereses_cesantias_mainjob/12
egen prestaciones_sociales_mainjob = rowtotal(prima_servicios_mainjob cesantias_mainjob intereses_cesantias_mainjob),missing
}

if (lbr_inc_monthly2<`piso_sintegral'*`minimum_wage' & fuerza_trabajo2==1){

replace prima_servicios_secondjob = lbr_inc_monthly2*(P6426/12) if P6426>0 &(P6040-(P6426/12))>10             //Checking age f worker and the time reported as working in current job.
replace prima_servicios_secondjob = lbr_inc_monthly2 if P6426>12
replace prima_servicios_secondjob = prima_servicios_secondjob/12
replace cesantias_secondjob=lbr_inc_monthly2*(P6426/12) if P6426>0 &(P6040-(P6426/12))>10
replace cesantias_secondjob=lbr_inc_monthly2 if P6426>12
replace intereses_cesantias_secondjob=0.12*cesantias_secondjob
replace cesantias_secondjob = cesantias_secondjob/12
replace intereses_cesantias_secondjob= intereses_cesantias_secondjob/12
egen prestaciones_sociales_secondjob = rowtotal(prima_servicios_secondjob cesantias_secondjob intereses_cesantias_secondjob),missing
}


**Income aggregates for Labor
replace contribution_SSC_secondjob=0 if P7040 ==2
egen contribution_SSC_total=rowtotal(contribution_SSC_mainjob contribution_SSC_secondjob),missing
egen agg_labor_incomemonth =rowtotal (lbr_inc_monthly lbr_inc_monthly2),missing
egen total_cost_employer= rowtotal (agg_labor_incomemonth prestaciones_sociales_mainjob),missing 

**Informality module
//Informal workers: Attempt of Endogenous identification (Informality according to DANE´s definition is not possible, since the variable asking firm size is not available in the public version of the data. Parametrize as a function of health, pension, type of contract, hourly wage)
//Below some possibilities for the ENPH ( They render very different results. default: informal worker does not contribute to health and pension. More criteria welcomed)
// Only for main Job.

*Local activating module
loc informality "yes"                         // yes to activate informality module. Type no to turn off.
 

if "`informality'"== "yes"{
*Definition of a local that activates according to the informality criterium chosen:

loc inform "medio"                      //fuerte for our version of strong informality, according to Guataqui et al (2017): No pension/health contribution,verbal contracts and below minimum wage labor earnings
                                         // medio for informality as workers not contributing to pension AND health
										 //debil for informality as workers not contributing to pension OR health
										 
tab P6090 P6920
 
tab P6090 P6920 [iw=FEX_C]

//If "fuerte" and "medio" are chosen, no individual classified as informal reported labor income (no differences in the simulation. For other definitions for informality this might not hold) 
//Fuerte does not depend on reported work status (asalariado,independiente)
if "`inform'"== "fuerte"{
generate informalidad=.
replace informalidad=1 if (P6090==2 & P6920==2 & P6450==1 & lbr_inc_monthly<=737717) 
replace informalidad =0 if !(P6090==2 & P6920==2 & P6450==1 & lbr_inc_monthly<=737717)
table informalidad
table informalidad [iw=FEX_C]
egen miembros_informal =total(SECUENCIA_P==1 & informalidad==1),by(hogares)

generate informalidad_our=.                              //Uses our definition of work status, different from the one in the survey.  
replace informalidad_our=1 if (P6090==2 & P6920==2 & P6450==1 & lbr_inc_monthly<=737717) 
replace informalidad_our=0 if !(P6090==2 & P6920==2 & P6450==1 & lbr_inc_monthly<=737717)
table informalidad_our
table informalidad_our [iw=FEX_C]
egen miembros_informal_our =total(SECUENCIA_P==1 & informalidad_our==1),by(hogares)

*Checking for informals that could have a second job (Problematic. We assume informality in main job implies informality in the secondary)
tab informalidad P7040 if P7070!=0 [iw=FEX_C]
tab informalidad P7040 if (P7070!=0&P7070!=98&P7070!=99)
tab informalidad_our P7040 if P7070!=0 [iw=FEX_C]
tab informalidad_our P7040 if (P7070!=0&P7070!=98&P7070!=99)
gen SSC_contrib_informal = contribution_SSC_total
replace SSC_contrib_informal = 0 if informalidad_our==1

gen effe = contribution_SSC_total/ agg_labor_incomemonth     //effective tax rate (denominator: total labor income)
gen effe_with_inform = SSC_contrib_informal/agg_labor_incomemonth //effective tax rate (simulating informality)
gen effe_total_inform = SSC_contrib_informal/total_cost_employer  // effective tax rate (denominator: total cost to employee)

graph twoway scatter effe_total_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe_with_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 

graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth  if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth   if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 


}

if "`inform'"== "medio"{
generate informalidad=.
replace informalidad=1 if P6090==2 & P6920==2 &(fuerza_trabajo==1|fuerza_trabajo==2|fuerza_trabajo==3) 
replace informalidad =0 if !(P6090==2 & P6920==2)&(fuerza_trabajo==1|fuerza_trabajo==2|fuerza_trabajo==3)
table informalidad
table informalidad [iw=FEX_C]
egen miembros_informal =total(SECUENCIA_P==1 & informalidad==1),by(hogares)

generate informalidad_our=.
replace informalidad_our=1 if P6090==2 & P6920==2 &(fuerza_trabajo_our==1|fuerza_trabajo_our==2|fuerza_trabajo_our==3)
replace informalidad_our=0 if !(P6090==2 & P6920==2)&(fuerza_trabajo_our==1|fuerza_trabajo_our==2|fuerza_trabajo_our==3)
table informalidad_our
table informalidad_our [iw=FEX_C]
egen miembros_informal_our =total(SECUENCIA_P==1 & informalidad_our==1),by(hogares)

*Checking for informals that could have a second job (Problematic. We assume informality in main job implies informality in the secondary)
tab informalidad P7040 if P7070!=0 [iw=FEX_C]
tab informalidad P7040 if (P7070!=0&P7070!=98&P7070!=99)
tab informalidad_our P7040 if P7070!=0 [iw=FEX_C]
tab informalidad_our P7040 if (P7070!=0&P7070!=98&P7070!=99)
gen SSC_contrib_informal = contribution_SSC_total
replace SSC_contrib_informal = 0 if informalidad_our==1

gen effe = contribution_SSC_total/ agg_labor_incomemonth                          
gen effe_with_inform = SSC_contrib_informal/agg_labor_incomemonth 
gen effe_total_inform = SSC_contrib_informal/total_cost_employer  // effective tax rate (denominator: total cost to employee)

graph twoway scatter effe_total_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe_with_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 


graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth  if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth   if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 


}

if "`inform'"== "debil"{
generate informalidad=.
replace informalidad=1 if (P6090==2 | P6920==2) &(fuerza_trabajo==1|fuerza_trabajo==2|fuerza_trabajo==3) 
replace informalidad =0 if !(P6090==2 | P6920==2)&(fuerza_trabajo==1|fuerza_trabajo==2|fuerza_trabajo==3)
table informalidad [iw=FEX_C]
egen miembros_informal =total(SECUENCIA_P==1 & informalidad==1),by(hogares)

generate informalidad_our=.
replace informalidad_our=1 if (P6090==2 | P6920==2) &(fuerza_trabajo_our==1|fuerza_trabajo_our==2|fuerza_trabajo_our==3)
replace informalidad_our =0 if !(P6090==2 | P6920==2)&(fuerza_trabajo_our==1|fuerza_trabajo_our==2|fuerza_trabajo_our==3)
table informalidad_our
table informalidad_our [iw=FEX_C]
egen miembros_informal_our =total(SECUENCIA_P==1 & informalidad_our==1),by(hogares)

*Checking for informals that could have a second job (Problematic. We assume informality in main job implies informality in the secondary)
tab informalidad P7040 if P7070!=0 [iw=FEX_C]
tab informalidad P7040 if (P7070!=0&P7070!=98&P7070!=99)
tab informalidad_our P7040 if P7070!=0 [iw=FEX_C]
tab informalidad_our P7040 if (P7070!=0&P7070!=98&P7070!=99)

//UNDER CONSTRUCTION: Criteria to impute zeroes to contributions

*gen effe = contribution_SSC_total/ agg_labor_incomemonth                          //effective tax rate (denominator: total labor income)
*gen effe_with_inform = SSC_contrib_informal/agg_labor_incomemonth 
*gen effe_total_inform = SSC_contrib_informal/total_cost_employer  // effective tax rate (denominator: total cost to employee)

graph twoway scatter effe_total_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe_with_inform agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 

graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth  if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe effe_with_inform effe_total_inform agg_labor_incomemonth   if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 

}


}

gen effe = contribution_SSC_total/ agg_labor_incomemonth
gen effe_total = contribution_SSC_total/ total_cost_employer       

graph twoway scatter effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 

graph twoway scatter effe_total agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2), by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 
graph twoway scatter effe_total agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 

graph twoway scatter effe_total effe agg_labor_incomemonth if inrange(fuerza_trabajo_our,1, 2)&effe<=1, by(fuerza_trabajo_our) ytitle("SSCs as fraction of labor income") ylabel(,angle(horizontal)) xtitle("Labor Income") 



******Income tax Calculation********

local income_tax "no"               //yes to active income tax module
if "`income_tax'"== "yes"{

**Parameters:
loc valor_UVT 31859 

****Defining annual income by sources

**Modifying labor income according to the survey and the tax code


gen agg_labor_incometaxmonth== agg_labor_incomemonth - cond(missing(lbr_inc_monthly2), 0, lbr_inc_monthly2) //Exclude second job...not enough info to make annual
//gen agg_labor_incometaxmonth = agg_labor_incomemonth
*Including scholarships from employers (Formulario 210)
replace P8610S1=. if P8610S1==98|P8610S1==99
replace P8610S2=. if P8610S2==98|P8610S1==99
replace P8612S1=. if P8612S1==98|P8612S1==99
replace P8612S2=. if P8612S2==98|P8612S2==99
replace P1664S1=. if P1664S1==98|P1664S1==99
gen P8610S1_monthly=P8610S1/12
gen P8610S2_monthly=P8610S2/12
gen P8612S1_monthly=P8612S1/12
gen P8612S2_monthly=P8612S2/12
gen P1664S1_monthly=P1664S1/12
egen agg_labor_prelim== rowtotal(agg_labor_incometaxmonth P8610S1_monthly P8610S2_monthly P8612S1_monthly P8612S2_monthly P1664S1_monthly),missing
replace agg_labor_incometaxmonth=agg_labor_prelim
drop agg_labor_prelim

//Note: Include cesantias

*Annual labor income (assumes no wage variation within a year)

gen annual_labor_income = P6426*agg_labor_incometaxmonth if  P6426>0 &(P6040-(P6426/12))>10 
replace annual_labor_income = 12*agg_labor_incometaxmonth if P6426>12
*Checking for underestimation of annual income (people could have other jobs during the year)
gen under_estimation = 0
replace under_estimation = 1 if P6790>P6426
tab under_estimation
tab under_estimation [iw=FEX_C]                        
sum lbr_inc_monthly if probada ==1 //16819 obs, 3,4 million people with labor income in a wide interval

*Pension income
*Annual pension income 
gen annual_pension_income=P7500S2A1*12            //we assume pension is granted during the whole year [?]
 
**Capital income

//Year:
*P7510S5A1
*P7513S6A1
*P7513S7A1
*P7513S5A1
*P7510S9A1

//Month, mostly rental variables (what to do? I will multiply by 12):
*P7500S1A1
*P7500S4A1
*P7500S5A1

gen annual_capital_income = rowtotal (P7510S5A1 P7513S6A1 P7513S7A1 P7513S5A1 P7510S9A1 12*P7500S1A1 12*P7500S4A1 12*P7500S5A1), missing

**non-labor income





**Dividends (to be defined, probably using IEFIC)

*Renta Líquida (Voluntary contributions to pension funds or food purchased to a worker from a third party are not included)
gen health_trabajador_year = P6426*health_mainjob_trabajador if  P6426>0 &(P6040-(P6426/12))>10
replace health_trabajador_year = 12*health_mainjob_trabajador if P6426>12
gen pension_trabajador_year =P6426*pension_mainjob_trabajador if  P6426>0 &(P6040-(P6426/12))>10
replace pension_trabajador_year = 12*pension_mainjob_trabajador if P6426>12
gen health_employer_year = P6426*health_mainjob_employer if  P6426>0 &(P6040-(P6426/12))>10
replace health_employer_year = 12*health_mainjob_employer if P6426>12
gen pension_employer_year = P6426*pension_mainjob_employer if  P6426>0 &(P6040-(P6426/12))>10
replace pension_employer_year = 12*pension_mainjob_employer if P6426>12


egen ingresos_no_renta=rowtotal(health_trabajador_year pension_trabajador_year health_employer_year pension_employer_year P8612S1 P8612S2 P1664S1 P8610S1 P8610S2),missing
gen renta_liquida =  annual_labor_income-ingresos_no_renta

*Renta Líquida cedular trabajo
*Consider exemptions and deductions. They cannot exceed 40% of renta líquida
gen deductions_income

P6630S6A1 
gen exemptions_income               //25% 


**Calculating tax from labor and pension

}
foreach x in DIRECTORIO SECUENCIA_ENCUESTA SECUENCIA_P ORDEN FEX_C ug fuerza_trabajo fuerza_trabajo2 miembros_hogar miembros_asal miembros_indep miembros_no_rem miembros_desoc miembros_inac lbr_inc_monthly lbr_inc_monthly2 lbr_inc_monthly3 informalidad miembros_informal health_mainjob_trabajador pension_mainjob_trabajador health_mainjob_employer pension_mainjob_employer parafiscales_mainjob cajas_mainjob health_secondjob_trabajador pension_secondjob_trabajador health_secondjob_employer pension_secondjob_employer parafiscales_secondjob cajas_secondjob fuerza_trabajo_our contribution_SSC_mainjob contribution_SSC_secondjob contribution_SSC_total agg_labor_incomemonth total_cost_employee effe_total effe{
glo names = "$names `x'"
}

//keep $names
//save "$direct\SSC_motrico", replace
//export delim $names using "$direct\SSC_motrico", nolabel replace  /*

*Average effective rate by decile

