import { Injectable } from '@angular/core';
import { Module } from './module.model';

@Injectable({
  providedIn: 'root'
})
export class ModuleService {
  filteredObjects(ToFilter: Module[], lang: string, searchTerm: string): Module[] {
    return ToFilter.filter(obj => obj.name[lang].toLowerCase().includes(searchTerm.toLowerCase()));
  }
}

