import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
imagenes = [
    'assets/img1.jpg',
    'assets/img2.jpg',
    'assets/img3.jpg',
    // Pon aquí las rutas de tus imágenes
  ];
  imagenActual = 0;

  anterior() {
    this.imagenActual = (this.imagenActual === 0) ? this.imagenes.length - 1 : this.imagenActual - 1;
  }

  siguiente() {
    this.imagenActual = (this.imagenActual === this.imagenes.length - 1) ? 0 : this.imagenActual + 1;
  }
}
