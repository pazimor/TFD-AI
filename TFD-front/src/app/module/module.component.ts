import {AfterViewInit, Component, ElementRef, inject, input, InputSignal, ViewChild} from '@angular/core';
import {DragDropModule} from '@angular/cdk/drag-drop';
import { Module } from './module.model';
import { CommonModule } from '@angular/common';
import { appStore } from '../store/data.store';

@Component({
  imports: [CommonModule, DragDropModule],
  selector: 'Module-item',
  templateUrl: './module.component.html',
  styleUrls: ['./module.component.scss', './modules-tiers.scss']
})

export class ModuleComponent {
  readonly currentModule: InputSignal<Module> = input.required<Module>()
  readonly store = inject(appStore);

  @ViewChild('statsDiv') statsDiv!: ElementRef;
  // Initialisez un tableau pour les objets sélectionnés
  showTooltip = false;

  language$$ = this.store.language;

  onTooltipEnter() {
    // On l’affiche (classe .show => display: block)
    this.showTooltip = true;

    // On attend le rendu pour pouvoir mesurer la tooltip
    setTimeout(() => {
      if (!this.statsDiv) return;

      // Récupère la position de la tooltip
      const tooltipRect = this.statsDiv.nativeElement.getBoundingClientRect();

      // Pour la taille de l'écran :
      const screenWidth = window.innerWidth || document.documentElement.clientWidth;

      // Vérifie si la tooltip dépasse à droite
      if (tooltipRect.right > screenWidth) {
        this.statsDiv.nativeElement.classList.add('flipLeft');
      } else {
        this.statsDiv.nativeElement.classList.remove('flipLeft');
      }
    }, 0); // On peut aussi utiliser requestAnimationFrame
  }

  onTooltipLeave() {
    // On masque la tooltip
    this.showTooltip = false;
    // On retire la classe flipLeft pour la prochaine fois
    if (this.statsDiv) {
      this.statsDiv.nativeElement.classList.remove('flipLeft');
    }
  }
}
