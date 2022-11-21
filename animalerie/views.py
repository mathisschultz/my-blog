from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import MoveForm
from .models import Animal, Equipement

def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animaux':animaux, 'equipements':equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if request.method == "POST":
        form=MoveForm(request.POST, instance=animal)
        if form.is_valid():
            if form.data['lieu'] == "Aquarium":
                ancien_lieu.disponibilite = "Libre"
                ancien_lieu.save()
                form.save(commit=False)
                if animal.etat == 'Endormi':
                    animal.etat = 'Affamé'
                    animal.save()
                    return redirect('animal_detail', id_animal=id_animal)
                else:
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'est pas endormi."})

            elif form.data['lieu'] == "algue à déguster":
                form.save(commit=False)
                if  animal.etat == 'Affamé':
                    if animal.lieu.disponibilite == 'Libre':
                        ancien_lieu.disponibilite = "Libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupé"
                        nouveau_lieu.save()
                        animal.etat = 'Repus'
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé les algues sont entrain d'être dévoré."})

                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas faim."})

            elif form.data['lieu'] == "Rocher de jeu":
                form.save(commit=False)
                if animal.etat == 'Repus':
                    if animal.lieu.disponibilite == 'Libre':
                        ancien_lieu.disponibilite = "Libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupé"
                        nouveau_lieu.save()
                        animal.etat = 'Fatigué'
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé le rocher est occupée."})
                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas envie de faire du sport."})

            else : #nid
                form.save(commit=False)
                if animal.etat == 'Fatigué':
                    if animal.lieu.disponibilite == 'Libre':
                        ancien_lieu.disponibilite = "Libre"
                        ancien_lieu.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
                        nouveau_lieu.disponibilite = "Occupé"
                        nouveau_lieu.save()
                        animal.etat = 'Endormi'
                        animal.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        return render(request, "animalerie/animal_detail.html", {'message': f"Désolé le coquillage est occupé."})
                else :
                    return render(request, "animalerie/animal_detail.html", {'message': f"Désolé {id_animal} n'a pas envie de dormir."})

        else:
            form = MoveForm()
            return render(request,
                    'animalerie/animal_detail.html',
                    {'animal': animal, 'lieu': animal.lieu, 'form': form})
    else:
        form = MoveForm()
        return render(request,
                'animalerie/animal_detail.html',
                {'animal': animal, 'lieu': animal.lieu, 'form': form})


def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    return render(request, 'animalerie/equipement_detail.html', {'equipement': equipement})