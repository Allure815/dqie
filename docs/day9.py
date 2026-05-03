Python 3.10.10 (tags/v3.10.10:aad5f6a, Feb  7 2023, 17:20:36) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> def classify_query(query):
... 	query = query.upper()
... 
... 	if query.startswith("SELECT"):
... 	   return "SELECT"
... 	elif query.startswith("INSERT"):
... 	   return "INSERT"
... 	elif query.startswith("UPDATE"):
... 	   return "UPDATE"
... 	 elif query.startswith("DELETE"):
... 	   return "DELETE"
... 	 else:
... 	 	  return "OTHER"
