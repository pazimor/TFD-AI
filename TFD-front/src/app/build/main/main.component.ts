import { Component, signal, computed, inject, OnInit, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { buildStore } from '../../store/build.store';
import { loginStore } from '../../store/login.store';
import { WeaponBuildComponent } from '../weapon/weapon.component';
import { DescedantBuildComponent } from '../descendant/descendant.component';
import { visualStore } from '../../store/display.store';
import { getUILabel } from '../../lang.utils';
import { ActivatedRoute } from '@angular/router';
import { dataStore } from '../../store/data.store';
import { defaultDescendants } from '../../types/descendant.types';
import { defaultModule } from '../../types/module.types';
import { defaultWeapon } from '../../types/weapon.types';
import { defaultReactor } from '../../types/reactor.types';
import { defaultExternalComponent } from '../../types/external.types';

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
  readonly visual_store = inject(visualStore);
  readonly data_store = inject(dataStore);
  private route = inject(ActivatedRoute);

  buildName = '';

  weapons = signal<number>(0);
  descendants = signal<number>(0);

  readonly _saveEffect = effect(() => {
    const resource = this.build_store.SaveBuildResource;
    if (resource?.hasValue()) {
      this.build_store.setBuildID(resource.value().build_id)
    }
  });

  readonly _loadEffect = effect(() => {
    const weaponsCount = this.build_store.weapons()
      .filter(w => w.weapon_id !== 0).length;
    this.weapons.set(weaponsCount);
    const hasDescendant = this.build_store.descendant().descendant_id !== 0;
    this.descendants.set(hasDescendant ? 1 : 0);
  });

  readonly _hydrateEffect = effect(() => {
    if (this.build_store.getBuildRessource.hasValue()) {
      const build = this.build_store.getBuildRessource.value()!.build_data;
      const data = {
        descendant: this.data_store.descendantResource.value()?.find(item => item.descendant_id === build.descendant) ?? defaultDescendants,
        descendantModules: build.descendantModules.map(id => this.data_store.modulesResource.value()?.find(item => item.module_id === id) ?? defaultModule),
        weapons: build.weapons.map(id => this.data_store.weaponResource.value()?.find(w => w.weapon_id === id) ?? defaultWeapon),
        weaponsModules: build.weaponsModules.map(slot => slot.map(id => this.data_store.modulesResource.value()?.find(m => m.module_id === id) ?? defaultModule)),
        reactor: this.data_store.reactorResource.value()?.find(item => item.reactor_id === build.reactor) ?? defaultReactor,
        externals: build.externals.map(id => this.data_store.externalResource.value()?.find(e => e.external_component_id === id) ?? defaultExternalComponent),
      };
      this.build_store.hydrate(data);
    }
  });

  weaponRange = computed(() => Array.from({ length: this.weapons() }));

  addWeapon() { this.weapons.update(v => Math.min(3, v + 1)); }
  removeWeapon() { this.weapons.update(v => Math.max(0, v - 1)); }

  addDescendant() { this.descendants.update(v => Math.min(1, v + 1)); }
  removeDescendant() { this.descendants.update(v => Math.max(0, v - 1)); }

  saveBuild() {
    const userId = this.login_store.user()?.id;

    if (!userId) {
      console.error('User ID not found. Cannot save build.');
      alert('User information not found. Cannot save build.'); // User-facing feedback
      return;
    }

    if (!this.buildName) {
      console.error('Build name is required.');
      alert('Build name is required.'); // User-facing feedback
      return;
    }

    this.build_store.saveToApi(userId, this.buildName);
  }

  ngOnInit(): void {
    this.data_store.load_all();
    this.route.queryParamMap.subscribe(params => {
      const idParam = params.get('build');
      if (idParam) {
        const buildId = Number(idParam);
        if (!Number.isNaN(buildId)) {
          this.build_store.loadFromApi(buildId);
        }
      }
    });
  }

  label(key: Parameters<typeof getUILabel>[1]) {
    return getUILabel(this.visual_store.get_lang(), key);
  }
}
