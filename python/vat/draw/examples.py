the_data = pd.DataFrame([1,2,7,2,7],columns=["x"])
draw_cdf( the_data["x"] )
if True: # alternatives
  # plt.show()
  plt.savefig("test.png")
