
from flet import *

import os
from supabase import create_client, Client
from dotenv import load_dotenv
import flet_fastapi
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)








async def main(page:Page):
    page.bgcolor="grey"
    nametext=TextField(label="Name",color="cyan")
    agetext=TextField(label="Age",color="cyan")
    edit_nametext=TextField(label="Name",color="cyan")
    edit_agetext=TextField(label="Age",color="cyan")
    id_value=""
    async def deletebtn(e):
        try:
            supabase.table('user').delete().eq('id', e.control.data['id']).execute()
            mydt.rows.clear()
            await load_data()
            page.snack_bar=SnackBar(                
                Text("Borrado!",size=20,text_align="CENTER"),
                duration=1000,              
                bgcolor="Red"
                )
            page.snack_bar.open=True
            await page.update_()

        except Exception as er:
            print ("Error en borrado", er)
        
                           
    async def savedata(e):
        try:
            global id_value            
            supabase.table('user').update({'name':edit_nametext.value, 'edad':edit_agetext.value}).eq('id', id_value).execute()
            dialog.open=False
            edit_agetext.value=""
            edit_nametext.value=""            
            id_value=""
            mydt.rows.clear()
            await load_data()
            page.snack_bar=SnackBar(
                Text("Actualizado!",size=20,text_align="CENTER"),
                bgcolor="green",
                duration=1000)
            page.snack_bar.open=True
            await page.update_async()


        except Exception as er:
            print(er,"error de update!")

    dialog=AlertDialog(
        title=Text("Edit data"),
        content=Column([
            edit_nametext,
            edit_agetext
        ]),
        actions=[TextButton("Guardar",on_click=savedata)]
    )    
    async def editbtn(e):
        global id_value
        edit_nametext.value=e.control.data["name"]
        edit_agetext.value=e.control.data["edad"]
        id_value=e.control.data["id"]
        page.dialog=dialog
        dialog.open=True
        await page.update_async()
       
    async def load_data():
        response = supabase.table('user').select("*").execute()

        for row in response.data:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["id"])),
                        DataCell(Text(row["name"])),
                        DataCell(Text(row["edad"])),
                        DataCell(
                            Row([
                                IconButton("delete",icon_color="red",data=row,on_click=deletebtn),
                                IconButton("create",icon_color="cyan",data=row,on_click=editbtn),

                            ])
                        ),
                        
                    ]
                )
            )
        await page.update_async()
        


    async def addtodb(e):
        try:
            supabase.table('user').insert({"edad": agetext.value, "name":nametext.value}).execute()
            mydt.rows.clear()
            await load_data()
            page.snack_bar=SnackBar(
                Text("Agregado!",size=20,text_align="CENTER"),
                bgcolor="green",
                duration=1000)
            page.snack_bar.open=True
            await page.update_async()

        except Exception as e:
            print("error! ",e)
        
        nametext.value=""
        agetext.value=""
        await page.update_async()


    mydt=DataTable(
        columns=[
            DataColumn(Text('id')),
            DataColumn(Text('Name')),
            DataColumn(Text('Age')),
            DataColumn(Text('Controls')),
        
        ],
        rows=[]
    )

    await page.add_async(
        Column([
            nametext,
            agetext,
            ElevatedButton("Add data", on_click=addtodb),
            mydt
        ])
    )

    await load_data()

directorio=os.getcwd()+"/assets"
app = flet_fastapi.app(main,assets_dir=str(directorio))
#app(target=main, assets_dir="assets")