plt.close()
draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                xmin = 1,
                 logx = True)
draw.savefig( vat_pics_dir + "purchases" , "quantity" )

plt.close()
draw.single_cdf( purchases["frequency"], "CDF of purchase frequency",
                 logx = True)
draw.savefig( vat_pics_dir + "purchases" , "frequency-cdf" )

plt.close()
plt.title("Purchase frequency")
plt.xticks( np.arange(1,11,1),
            ["Diario"
             , "\"Varias veces\n por semana\""
             , "Semanal"
             , "Quincenal"
             , "Mensual"
             , "Bimestral"
             , "Trimestral"
             , "Anual"
             , "\"Esporádico\""
             , "Semestral"],
            rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.30) # labels go out of frame otherwise
draw.table( purchases, "frequency-code" )
draw.savefig( vat_pics_dir + "purchases" , "frequency" )

plt.close()
draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                 logx = True)
draw.savefig( vat_pics_dir + "purchases" , "value" )

plt.close()
draw.single_cdf( purchases["vat-paid"], "CDF of VAT paid per purchase",
                 logx = True)
draw.savefig( vat_pics_dir + "purchases" , "vat-in-pesos" )
