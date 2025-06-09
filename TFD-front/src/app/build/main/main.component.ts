import { Component, signal, computed, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../env/environment';
import { buildStore } from '../../store/build.store';
import { loginStore } from '../../store/login.store';
import { WeaponBuildComponent } from '../weapon/weapon.component';
import { DescedantBuildComponent } from '../descendant/descendant.component';

@Component({
  standalone: true,
  selector: 'main-build',
  imports: [CommonModule, FormsModule, WeaponBuildComponent, DescedantBuildComponent],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss', '../../../styles.scss']
})
export class MainBuildComponent implements OnInit {
  readonly build_store = inject(buildStore);
  readonly login_store = inject(loginStore);
  constructor(private http: HttpClient) {}

  buildName = '';

  weapons = signal<number>(0);
  descendants = signal<number>(0);

  // convenience computed signal that yields an array of length `weapons()`
  weaponRange = computed(() => Array.from({ length: this.weapons() }));

  addWeapon() { this.weapons.update(v => Math.min(3, v + 1)); }
  removeWeapon() { this.weapons.update(v => Math.max(0, v - 1)); }

  addDescendant() { this.descendants.update(v => Math.min(1, v + 1)); }
  removeDescendant() { this.descendants.update(v => Math.max(0, v - 1)); }

  saveBuild() {
    const userId = this.login_store.user()?.id;
    if (!userId || !this.buildName) { return; }
    const data = this.build_store.serialize();

    //TODO: implement this requests inside the build_store and call it
    this.http.post(`${environment.apiBaseUrl}/builds`, {
      user_id: userId,
      name: this.buildName,
      data,
    }, { withCredentials: true }).subscribe();
  }

  ngOnInit(): void {
    const params = new URLSearchParams(window.location.search);
    const idParam = params.get('build');
    if (idParam) {
      const buildId = Number(idParam);
      if (!Number.isNaN(buildId)) {
        this.build_store.loadFromApi(buildId);
      }
    }
  }
}
