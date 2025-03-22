import { Injectable } from '@angular/core';
import { Module } from './module.model';

@Injectable({
  providedIn: 'root'
})
export class ModuleService {

  // warning categories has to be parsed !!!
  // for one type of ammo the name is not the same
  // on modules and on weapon so it has to change on database
  filteredObjects(ToFilter: Module[], lang: string, searchTerm: string, categories: string): Module[] {
    const parts = categories.split(', ')
    if (parts[parts.length - 1]) {
      categories = parts[parts.length - 1]
    }
    return ToFilter.filter(obj => obj.type.includes(categories)).filter(obj => obj.name[lang].toLowerCase().includes(searchTerm.toLowerCase()));
  }

  getContraint (mod: Module): string {
    const parts = mod.type.split(",");
    return parts.length > 1 ? parts[1].trim() : "None";
  }
}

