from flask import Flask, render_template, request
import math
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = ""
    bmi_status = ""
    whtr = ""
    whtr_status = ""
    rfm = ""
    rfm_status = ""
    absi = ""
    absi_status = ""
    navy_method = ""
    navy_method_status = ""
    final_conclusion = ""
    recommendations = ""
    absi_z = ""

    if request.method == "POST":
        sex = request.form.get("gender")
        age = int(request.form.get("ageInput"))
        height = float(request.form.get("heightInput")) 
        mass = float(request.form.get("massInput"))
        wc = float(request.form.get("waistInput"))
        neck = float(request.form.get("neckInput"))
        hip = float(request.form.get("hipsInput"))
        sport = request.form.get("sport")
        height_m = height / 100 # см → метри
        height_d = height / 2.54
        wc_m = wc /100
        # викликаємо функцію
        bmi, bmi_status = BMI(mass, height_m)
        whtr, whtr_status = WHtR(height, wc)
        rfm, rfm_status = RFM(sex, height, wc, age, neck, hip)
        absi, absi_status, absi_z = ABSI(height_m, wc_m, mass, age, sex)
        final_conclusion, recommendations = make_conclusion (bmi, whtr, rfm, absi, absi_z, sex)

        #navy_method, navy_method_status = Navy_method (sex, wc, neck, height, hip)
         

    return render_template("index.html", bmi = bmi, bmi_status = bmi_status,
                           whtr = whtr, whtr_status = whtr_status,
                           rfm = rfm, rfm_status = rfm_status,
                           absi = absi, absi_status = absi_status, absi_z = absi_z,
                           navy_method = navy_method, navy_method_status = navy_method_status,  final_conclusion=final_conclusion,
                           recommendations=recommendations)


def BMI(m, h):
    iimt = m / (h ** 2)

    if iimt < 18.5:
        status = f"BMI - {iimt:.1f}"
    elif 18.5 <= iimt <= 24.9:
        status = f"BMI - {iimt:.1f}"
    elif 24.9 < iimt < 30:
        status = f"BMI - {iimt:.1f}"
    else:
        status = f"BMI - {iimt:.1f}"

    return round(iimt, 1), status

# Індекс центрального ожиріння (WHtR)  WC — окружність талії H — зріст (у тих самих одиницях)  норма WHtR<0.5

def WHtR(height, wc):
  index_central_adiposity = wc / height
  status = f"WHtR - {index_central_adiposity:.1f}"
  print(f"WHtR- {index_central_adiposity:.1f}")
  return round(index_central_adiposity,2), status 

""""
#  Формула Navy Method (ВМС США)
def Navy_method (sex, wc, neck, height, hip):
    if wc + hip <= neck:
      return None, "Помилка вимірів. Введи правельні параметри"
  
    if sex == "male":
        bf = 86.010 * math.log10(wc - neck) - 70.041 * math.log10(height) + 36.76 
        print(f"твій % жиру в організмі складає {bf:.1f}% при нормі 14% - 25%") 
        status = f"твій % жиру в організмі складає {bf:.1f}% при нормі 14% - 25%" 
          
    elif sex == "female":
        bf = 163.205 * math.log10(wc + hip - neck) - 97.684 * math.log10(height) - 78.387 
        print(f"твій % жиру в організмі складає {bf:.1f}% при нормі 20% - 34%")  
        status = f"твій % жиру в організмі складає {bf:.1f}% при нормі 20% - 34%"  
    return round(bf, 1),status
"""
# 4. Формула відсотка жиру (RFM — Relative Fat Mass) 
def RFM(sex, height, wc, age, neck, hip):
    if age < 15:
        print (None, None, "RFM не застосовується до 15 років")
        return None, None, "RFM не застосовується до 15 років"       
    if sex == "male":
        relative_fat_mass = (64-(20*(height/wc)) + 0.2 * (age - 20))
        bf = 86.010 * math.log10(wc - neck) - 70.041 * math.log10(height) + 36.76 
        medium_index = (relative_fat_mass + bf) / 2
        if medium_index < 14:
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%, це дуже низизький рівень. Норма > 14% ")    
            status = f"RFM - {medium_index:.0f}%"    
        elif 14 <= medium_index <= 25:
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%")
            status = f"RFM - {medium_index:.0f}%"
        elif 25 < medium_index <= 31:       
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%, це підвищений рівень. Норма - до 25%")
            status = f"RFM - {medium_index:.0f}%"
        elif medium_index > 31:       
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%, це ожиріння!!! Норма - до 25% ")    
            status = f"RFM - {medium_index:.0f}%"    
        return round(medium_index, 1), status    
        
    if sex == "female":
        relative_fat_mass = (76-(20*(height/wc))+ 0.2 * (age - 20))
        bf = 163.205 * math.log10(wc + hip - neck) - 97.684 * math.log10(height) - 78.387
        medium_index = (relative_fat_mass + bf) / 2
        if medium_index <= 20:
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}, це дуже низизький рівень")    
            status = f"RFM - {medium_index:.0f}"    
        elif 20 < medium_index <= 34:
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}, це в межах норми")
            status = f"RFM - {medium_index:.0f}%"
        elif 34 < medium_index <= 39:       
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%, це підвищений рівень. Зверни увагу!")
            status = f"RFM - {medium_index:.0f}%"
        elif medium_index >= 39:       
            print(f"Відсоток жиру в твоєму тілі складає {medium_index:.0f}%, це ожиріння!") 
            status = f"RFM - {medium_index:.0f}%" 
            
        return round(medium_index, 1), status 
    return None, "Не вибрано стать!"




# A Body Shape Index (ABSI). оцінка ризику для здоров’я, пов’язаного з абдомінальним жиром.
def ABSI(height_m, wc_m, mass, age, sex):
    if age < 18:
        return None, "ABSI не застосовується до 18 років"
    bmi_m = mass / (height_m ** 2)
    body_shape_index = wc_m / ((bmi_m**(2/3))*(height_m** 0.5))
   
    if sex == "male":
        if  5 <= age < 10:
            u = 0.08009
            q = 0.00335

        elif  10 <= age < 15:
            u = 0.07969
            q = 0.00408

        elif  15 <= age < 20:
            u = 0.08060
            q = 0.00430
    
        elif  20 <= age < 25:
            u = 0.08085
            q = 0.00438   
        
        elif  25 <= age < 30:
            u = 0.08110
            q = 0.00447
        
        elif  30 <= age < 35:
            u = 0.08124
            q = 0.00455  
        
        elif  35 <= age < 40:
            u = 0.08129
            q = 0.00460        
     
        elif  40 <= age < 45:
            u = 0.08134
            q = 0.00465 
        
        elif  45 <= age < 50:
            u = 0.08139
            q = 0.00471 
        
        elif  50 <= age < 55:
            u = 0.08144
            q = 0.00477  
        
        elif  55 <= age < 60:
            u = 0.08149
            q = 0.00482              
    
        elif  60 <= age < 65:
            u = 0.08154
            q = 0.00487
        
        else:
            u = 0.08159
            q = 0.00492
            
  
    if sex == "female":
        if  5 <= age < 10:
           u = 0.07910
           q = 0.00328

        elif  10 <= age < 15:
           u = 0.07960
           q = 0.00370

        elif  15 <= age < 20:
           u = 0.07982
           q = 0.00380
    
        elif  20 <= age < 25:
           u = 0.07992
           q = 0.00390
        
        elif  25 <= age < 30:
           u = 0.08002
           q = 0.00400
        
        elif  30 <= age < 35:
           u = 0.08012
           q = 0.00410  
        
        elif  35 <= age < 40:
           u = 0.08022
           q = 0.00420
        
        elif  40 <= age < 45:
           u = 0.08032
           q = 0.00430 
           
        elif  45 <= age < 50:
           u = 0.08042
           q = 0.00440 
           
        elif  50 <= age < 55:
           u = 0.08052
           q = 0.00450                 
        
        elif  55 <= age < 60:
           u = 0.08062
           q = 0.00460 
           
        elif  60 <= age < 65:
           u =0.08072
           q = 0.00470
           
        else:
           u =0.08082
           q = 0.00480        
           
           
    z_score = (body_shape_index - u)/q  
    if z_score <= -0.868:
        print(f"твій індекс ABSI - {body_shape_index:.3f} -за шкалою z-score ти маєш дуже низький ризик кардіометаболічних захворювань, пов’язаних із абдомінальним  жиром.")
        status = f"твій індекс ABSI - {body_shape_index:.3f}" 
    elif -0.868  < z_score <= -0.272:
        print(f"твій індекс ABSI - {body_shape_index:.3f} -за шкалою z-score ти маєш низький ризик  кардіометаболічних захворювань, пов’язаних із абдомінальним (вісцеральним) жиром.")
        status = f"твій індекс ABSI - {body_shape_index:.3f}" 
    elif  -0.272 < z_score <= 0.229:
        print(f"твій індекс ABSI - {body_shape_index:.3f} -за шкалою z-score ти маєш помірний ризик  кардіометаболічних захворювань, пов’язаних із абдомінальним (вісцеральним) жиром.")
        status = f"твій індекс ABSI - {body_shape_index:.3f}"
    elif  0.229 < z_score <= 0.798:
        print(f"твій індекс ABSI - {body_shape_index:.3f} -за шкалою z-score ти маєш високий ризик смертності та кардіометаболічних захворювань, пов’язаних із абдомінальним (вісцеральним) жиром.")
        status = f"твій індекс ABSI - {body_shape_index:.3f}"
    elif  0.798 < z_score:
        print(f"твій індекс ABSI - {body_shape_index:.3f} -за шкалою z-score ти маєш дуже високий ризик смертності та кардіометаболічних захворювань, пов’язаних із абдомінальним (вісцеральним) жиром.")    
        status = f"твій індекс ABSI - {body_shape_index:.3f}"  
    return round(body_shape_index, 3), status, z_score   


def make_conclusion(bmi, whtr, rfm, absi, absi_z, sex):

    conclusion = ""
    rec = []

    # --- АНАЛІЗ BMI ---
    if bmi:
        if bmi < 18.5:
            conclusion += "Виявлено дефіцит маси тіла. "
            rec.append("Збільшити калорійність раціону та додати силові тренування.")
        elif 18.5 <= bmi <= 24.9:
            conclusion += "Маса тіла в межах норми. "
        elif 25 <= bmi < 30:
            conclusion += "Спостерігається надмірна маса тіла. "
            rec.append("Рекомендується контроль калорій та збільшення фізичної активності.")
        else:
            conclusion += "Ознаки ожиріння. "
            rec.append("Необхідно зниження ваги під контролем харчування та активності.")

    # --- WHtR (жир на животі) ---
    if whtr:
        if whtr >= 0.5:
            conclusion += "Є підвищене накопичення абдомінального жиру. "
            rec.append("Зменшити окружність талії: кардіо + дефіцит калорій.")

    # --- RFM (жир %) ---
    if rfm:
        if sex == "male":
          if rfm < 14:           
            conclusion += "Дуже низький відсоток жиру. "
            rec.append("Рекомендовано висококалорійну дієту та тренування.") 
          elif 14 <= rfm <= 25:       
            conclusion += "Відсоток жиру в твоєму тілі в межах норми"          
          elif 25 < rfm <= 31:                   
            conclusion += "Підвищений відсоток жиру. "
            rec.append("Корекція харчування + тренування.")
          elif rfm > 31:           
            conclusion += "Ожиріння! "
            rec.append("Низькокалорійна дієта, збільшити рухову активність, тренування.")  
        if sex == "female":
            if rfm > 34:
                conclusion += "Високий відсоток жиру. "
                rec.append("Рекомендується контроль ваги та активність.")

     
        
        
    

    # --- ABSI (ризик через z-score) ---
    if absi_z is not None:
      if absi_z > 0.798:
        conclusion += "Ти маєш дуже високий ризик кардіометаболічних захворювань "
        rec.append("Рекомендується консультація лікаря, корекція способу життя та підвищення фізичної активності.")
      elif absi_z > 0.229:
        conclusion += "Ти маєш високий ризик кардіометаболічних захворювань"
        rec.append("Зменшити абдомінальний жир за рахунок корекції раціону харчування, та підвищення фізичної активності.")
      elif absi_z > -0.272:
        conclusion += "Ти маєш помірний ризик кардіометаболічних захворювань "
        rec.append("Зменшити абдомінальний жир за рахунок підвищення фізичної активності.")
      elif absi_z > -0.868:
        conclusion += "Ти маєш низький ризик кардіометаболічних захворювань"
      else:
        conclusion += "Ти маєш дуже низький ризик кардіометаболічних захворювань."

    # --- якщо все ок ---
    if conclusion == "":
      conclusion = "За результатами розрахунків всі основні показники знаходяться в межах фізіологічної норми."
      rec.append("Рекомендується підтримувати поточний рівень фізичної активності та збалансоване харчування.")
    else:
      conclusion = "Загальний висновок: " + conclusion

    return conclusion, " ".join(rec)
    

if __name__ == "__main__":
    app.run(debug=True)