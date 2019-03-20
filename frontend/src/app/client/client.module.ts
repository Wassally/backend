import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { clientRoutingModule } from './client-routing.module';
import { MainComponent } from './main/main.component';


@NgModule({
  declarations: [HeaderComponent, MainComponent 
  ],
  imports: [
    CommonModule ,
    clientRoutingModule
  ]
})
export class ClientModule { }
