if True: # purchase quantity, logx and linear
  plt.close()
  draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                   xmin = 1, xmax = 1e3)
  draw.savefig( vat_pics_dir + "purchases" , "quantity" )
  
  plt.close()
  draw.single_cdf( purchases["quantity"], "CDF of quantity per purchase",
                  xmin = 1, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "quantity" )
  
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
draw.table( purchases, "frequency-code" )
draw.savefig( vat_pics_dir + "purchases" , "frequency" )

if True: # purchase value, logx and linear
  plt.close()
  draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                   xmin=1, xmax=1e5)
  draw.savefig( vat_pics_dir + "purchases" , "value" )

  plt.close()
  draw.single_cdf( purchases["value"], "CDF of monthly purchase value",
                   xmin =1, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "value" )

if True: # VAT per purchase, logx and linear  
  plt.close()
  draw.single_cdf( purchases["vat-paid"], "CDF of VAT paid per purchase",
                   xmin = 1, xmax = 1e4)
  draw.savefig( vat_pics_dir + "purchases" , "vat-in-pesos" )

  plt.close()
  draw.single_cdf( purchases["vat-paid"], "CDF of VAT paid per purchase",
                   xmin = 0.01, logx = True)
  draw.savefig( vat_pics_dir + "purchases/logx" , "vat-in-pesos" )
  
