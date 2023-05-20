from tkinter import *
import customtkinter
import openai
import os
import pickle

# Genel ayarlar
root=customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry("600x600")

#icon sayfası https://tkinter.com/images/ai_lt.ico
root.iconbitmap("ai_lt.ico")

#renklendirme özellikleri dark light
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Fonksiyonlar
def speak():
    if chat_entry.get():
        filename="api_key"
        try:
            if os.path.isfile(filename):
                input_file=open(filename,'rb')
                api_sifre=pickle.load(input_file)
                # my_text.insert(END, "\n\nÇalışıyor...")
                openai.api_key=api_sifre
                openai.Model.list()

                cevap=openai.Completion.create( 
                    model="text-davinci-003",
                    prompt=chat_entry.get(),
                    temperature=0,
                    max_tokens=4000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                my_text.insert(END, (cevap["choices"][0]["text"]).strip())
                my_text.insert(END, "\n\n")

            else:
                input_file=open(filename, 'wb')
                input_file.close()
                my_text.insert(END, "\n\n API key almayı unuttun lütfen aşağıdaki sayfadan temin ediniz...\n   https://platform.openai.com/account/api-keys")
        except Exception as e:
            my_text.insert(END, f"\n\n Bir hata oluştu: {e}")
    else:
        my_text.insert(END, "\n\n Hey dostum soru sormayı ununttun")


def clear():
    my_text.delete(1.0, END)
    chat_entry.delete(0, END)


def key():
    filename="api_key"
    try:

        if os.path.isfile(filename):
            input_file=open(filename, 'rb')
            api_sifre=pickle.load(input_file)
            api_entry.insert(END, api_sifre)
        else:
            input_file=open(filename, 'wb')
            input_file.close()
    except Exception as e:
        my_text.insert(END, f"\n\n Bir hata oluştu: {e}")    

    root.geometry("600x700")
    api_frame.pack(pady=10)
    

def save_key():
    filename="api_key"
    try:

        output_file=open(filename, 'wb')
        pickle.dump(api_entry.get(), output_file)
        api_entry.delete(0,END)
        api_frame.pack_forget()
    except Exception as e:
        my_text.insert(END, f"\n\n Bir hata oluştu: {e}")

    
    root.geometry("600x600")
    pass


#text frame
text_frame=customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

my_text=Text(text_frame, bg="#343638", fg="red", width=65, bd=1, relief="flat", wrap=WORD, selectbackground="#1f538d", font=("Arial", 11, "bold"))
my_text.grid(row=0,column=0)

#scrollbar
text_scroll=customtkinter.CTkScrollbar(text_frame, command=my_text.yview)
text_scroll.grid(row=0,column=1, sticky="ns")

my_text.configure(yscrollcommand=text_scroll.set)

#Entry
chat_entry=customtkinter.CTkEntry(root, placeholder_text="Chat GPT'ye ne sormak istersiniz?", width=495, height=50, border_width=1)
chat_entry.pack(pady=10)

#Button Frame
button_frame=customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

#Submit button
submit_button=customtkinter.CTkButton(button_frame, text="Chat-GPT'ye Sor", command=speak)
submit_button.grid(row=0,column=0, padx=20)

#Clear button
clear_button=customtkinter.CTkButton(button_frame, text="Cevapları Temizle", command=clear)
clear_button.grid(row=0,column=1, padx=20)

#API button
api_button=customtkinter.CTkButton(button_frame, text="API Key :Güncelle", command=key)
api_button.grid(row=0,column=2, padx=20)

#API Anahtarı Frame
api_frame=customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=10)

api_entry=customtkinter.CTkEntry(api_frame, placeholder_text="Yeni API Key Griniz", width=300, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

api_save_button=customtkinter.CTkButton(api_frame, text="Key Kaydet", command=save_key)

api_save_button.grid(row=0,column=1, padx=10)



root.mainloop()
