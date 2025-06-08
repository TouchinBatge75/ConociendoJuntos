import { Routes } from '@angular/router';
import { HomeComponent } from './component/home/home.component';
import { DestinosComponent } from './component/destinos/destinos.component';
import { NosotrosComponent } from './component/nosotros/nosotros.component';
import { PromocionesComponent } from './component/promociones/promociones.component';
import { ContactanosComponent } from './component/contactanos/contactanos.component';


export const routes: Routes = [
    {path: '', redirectTo: 'home', pathMatch: 'full'},
    {path: 'home', component: HomeComponent},
    {path: 'destinos', component: DestinosComponent},
    {path: 'nosotros', component: NosotrosComponent},
    {path: 'promociones', component: PromocionesComponent},
    {path: 'contactanos', component: ContactanosComponent},
];
