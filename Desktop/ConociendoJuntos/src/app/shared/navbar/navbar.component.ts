import { Component } from '@angular/core';
import { RouterModule, RouterLink, RouterLinkActive} from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})

export class NavbarComponent {
  menuAbierto = false;

  toggleMenu() {
    this.menuAbierto = !this.menuAbierto;
  }
}
